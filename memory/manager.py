
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class MemoryManager:
    """
    Persistent memory for the Agentic AI Assistant.

    Features:
    - Saves memories in a local SQLite database.
    - Retrieves relevant memories using keyword matching.
    - Keeps memories across sessions and application restarts.
    - Supports session-specific and global memories.
    """

    def __init__(self, db_path: str | Path | None = None):
        project_root = Path(__file__).resolve().parents[2]

        self.db_path = Path(db_path) if db_path else (
            project_root / "memory" / "agent_memory.db"
        )

        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_database()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(
            str(self.db_path),
            timeout=10,
        )
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize_database(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    category TEXT NOT NULL DEFAULT 'general',
                    session_id TEXT,
                    importance INTEGER NOT NULL DEFAULT 3,
                    created_at TEXT NOT NULL
                )
                """
            )

            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_memories_session
                ON memories(session_id)
                """
            )

    def add_memory(
        self,
        content: str,
        category: str = "general",
        session_id: str | None = None,
        importance: int = 3,
    ) -> int:
        """Save one memory and return its database ID."""
        content = content.strip()

        if not content:
            raise ValueError("Memory content cannot be empty.")

        importance = max(1, min(5, int(importance)))
        created_at = datetime.now(timezone.utc).isoformat()

        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO memories
                    (content, category, session_id, importance, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    content,
                    category.strip() or "general",
                    session_id,
                    importance,
                    created_at,
                ),
            )
            return int(cursor.lastrowid)

    def search_memories(
        self,
        query: str,
        limit: int = 5,
        session_id: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Find memories using simple keyword matching.

        Global memories are available to every session.
        Session-specific memories are available only to that session.
        """
        words = list(
            dict.fromkeys(
                word.lower()
                for word in query.split()
                if len(word.strip(".,!?;:\"'()[]{}")) >= 3
            )
        )

        if not words:
            return []

        limit = max(1, min(20, int(limit)))
        conditions = []
        parameters: list[Any] = []

        for word in words[:12]:
            conditions.append("LOWER(content) LIKE ?")
            parameters.append(f"%{word}%")

        visibility_condition = (
            "(session_id IS NULL OR session_id = ?)"
            if session_id
            else "session_id IS NULL"
        )

        if session_id:
            parameters.append(session_id)

        sql = f"""
            SELECT id, content, category, session_id, importance, created_at
            FROM memories
            WHERE ({' OR '.join(conditions)})
              AND {visibility_condition}
            ORDER BY importance DESC, id DESC
            LIMIT ?
        """
        parameters.append(limit)

        with self._connect() as connection:
            rows = connection.execute(sql, parameters).fetchall()

        return [dict(row) for row in rows]

    def get_context(
        self,
        query: str,
        session_id: str | None = None,
        limit: int = 5,
    ) -> str:
        """Format relevant memories for insertion into an LLM prompt."""
        memories = self.search_memories(
            query=query,
            limit=limit,
            session_id=session_id,
        )

        if not memories:
            return ""

        lines = [
            "Relevant memories from previous interactions:",
            "Use these only when relevant to the current request.",
        ]

        for memory in memories:
            lines.append(
                f"- [{memory['category']}] {memory['content']}"
            )

        return "\n".join(lines)

    def remember_turn(
        self,
        user_message: str,
        assistant_response: str,
        session_id: str | None = None,
    ) -> None:
        """
        Persist a completed conversation turn.

        This stores conversation text, not automatically extracted facts.
        """
        if user_message.strip():
            self.add_memory(
                content=f"User asked: {user_message.strip()}",
                category="conversation",
                session_id=session_id,
                importance=2,
            )

        if assistant_response.strip():
            self.add_memory(
                content=f"Assistant answered: {assistant_response.strip()}",
                category="conversation",
                session_id=session_id,
                importance=1,
            )

    def delete_memory(self, memory_id: int) -> bool:
        """Delete one memory by its ID."""
        with self._connect() as connection:
            cursor = connection.execute(
                "DELETE FROM memories WHERE id = ?",
                (memory_id,),
            )
            return cursor.rowcount > 0

    def clear_session(self, session_id: str) -> int:
        """Delete memories belonging to one session."""
        with self._connect() as connection:
            cursor = connection.execute(
                "DELETE FROM memories WHERE session_id = ?",
                (session_id,),
            )
            return cursor.rowcount

    def list_memories(self, limit: int = 50) -> list[dict[str, Any]]:
        """List the newest memories for inspection."""
        limit = max(1, min(200, int(limit)))

        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT id, content, category, session_id, importance, created_at
                FROM memories
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()

        return [dict(row) for row in rows]
