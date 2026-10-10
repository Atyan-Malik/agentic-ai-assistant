
import tkinter as tk
from tkinter import font
from datetime import datetime
import threading
import requests


# ============================================================
# Configuration
# ============================================================

APP_NAME = "CLI AI Assistant"
API_BASE_URL = "http://127.0.0.1:8000"
PROMPT = r"C:\CLI-AI>"


# ============================================================
# Terminal Application
# ============================================================

class TerminalApp:

    def __init__(self, root):

        self.root = root
        self.history = []

        # ----------------------------------------------------
        # Window
        # ----------------------------------------------------

        self.root.title(APP_NAME)
        self.root.geometry("950x600")
        self.root.minsize(700, 450)

        self.root.configure(bg="#000000")

        # ----------------------------------------------------
        # Fonts
        # ----------------------------------------------------

        self.terminal_font = font.Font(
            family="Consolas",
            size=11
        )

        self.prompt_font = font.Font(
            family="Consolas",
            size=11,
            weight="bold"
        )

        # ----------------------------------------------------
        # Main container
        # ----------------------------------------------------

        self.main_frame = tk.Frame(
            self.root,
            bg="#000000"
        )

        self.main_frame.pack(
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # Terminal output
        # ----------------------------------------------------

        self.output = tk.Text(
            self.main_frame,
            bg="#000000",
            fg="#F2F2F2",
            insertbackground="#FFFFFF",
            selectbackground="#333333",
            selectforeground="#FFFFFF",
            font=self.terminal_font,
            wrap="word",
            borderwidth=0,
            highlightthickness=0,
            padx=18,
            pady=15,
            spacing1=2,
            spacing3=2,
            state="disabled"
        )

        self.output.pack(
            side="top",
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # Scrollbar
        # ----------------------------------------------------

        scrollbar = tk.Scrollbar(
            self.main_frame,
            command=self.output.yview,
            bg="#111111",
            troughcolor="#000000",
            activebackground="#333333"
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.output.configure(
            yscrollcommand=scrollbar.set
        )

        # ----------------------------------------------------
        # Input area
        # ----------------------------------------------------

        self.input_frame = tk.Frame(
            self.main_frame,
            bg="#000000"
        )

        self.input_frame.pack(
            side="bottom",
            fill="x",
            padx=18,
            pady=(0, 15)
        )

        # Prompt

        self.prompt_label = tk.Label(
            self.input_frame,
            text=PROMPT,
            bg="#000000",
            fg="#00FF66",
            font=self.prompt_font
        )

        self.prompt_label.pack(
            side="left"
        )

        # Input

        self.input_entry = tk.Entry(
            self.input_frame,
            bg="#000000",
            fg="#FFFFFF",
            insertbackground="#FFFFFF",
            selectbackground="#333333",
            selectforeground="#FFFFFF",
            font=self.terminal_font,
            borderwidth=0,
            highlightthickness=0
        )

        self.input_entry.pack(
            side="left",
            fill="x",
            expand=True
        )

        # ----------------------------------------------------
        # Keyboard
        # ----------------------------------------------------

        self.input_entry.bind(
            "<Return>",
            self.handle_enter
        )

        self.root.bind(
            "<Control-l>",
            self.handle_clear
        )

        self.root.bind(
            "<Escape>",
            self.handle_exit
        )

        # ----------------------------------------------------
        # Startup
        # ----------------------------------------------------

        self.print_startup()
        self.input_entry.focus_set()

    # ========================================================
    # Output
    # ========================================================

    def write(self, text="", color="#F2F2F2"):

        self.output.configure(state="normal")

        tag_name = f"color_{color.replace('#', '')}"

        self.output.tag_configure(
            tag_name,
            foreground=color
        )

        self.output.insert(
            "end",
            text,
            tag_name
        )

        self.output.configure(state="disabled")
        self.output.see("end")

    # ========================================================
    # Startup Screen
    # ========================================================

    def print_startup(self):

       

        self.write(
            "                    CLI AI ASSISTANT\n",
            "#00FF66"
        )

       
        self.write(
            "\n"
            "  Personal AI assistant terminal interface\n"
           
            "\n",
            "#AAAAAA"
        )

        self.write(
            "  Type /help for available commands.\n\n",
            "#FFFFFF"
        )

    # ========================================================
    # Enter
    # ========================================================

    def handle_enter(self, event=None):

        user_input = self.input_entry.get().strip()

        if not user_input:
            return "break"

        self.input_entry.delete(
            0,
            "end"
        )

        # Display command

        self.write(
            f"{PROMPT} ",
            "#00FF66"
        )

        self.write(
            f"{user_input}\n",
            "#FFFFFF"
        )

        # Save history

        self.history.append(
            f"{PROMPT} {user_input}"
        )

        # Process command

        self.process_command(user_input)

        return "break"

    # ========================================================
    # Commands
    # ========================================================

    def process_command(self, user_input):

        command = user_input.lower().strip()

        # ----------------------------------------------------
        # Exit
        # ----------------------------------------------------

        if command in {
            "/exit",
            "/quit",
            "exit",
            "quit"
        }:

            self.write(
                "\nGoodbye!\n",
                "#00FF66"
            )

            self.root.after(
                500,
                self.root.destroy
            )

            return

        # ----------------------------------------------------
        # Help
        # ----------------------------------------------------

        if command == "/help":

            self.show_help()

            return

        # ----------------------------------------------------
        # Clear
        # ----------------------------------------------------

        if command == "/clear":

            self.clear_screen()

            return

        # ----------------------------------------------------
        # History
        # ----------------------------------------------------

        if command == "/history":

            self.show_history()

            return

        # ----------------------------------------------------
        # About
        # ----------------------------------------------------

        if command == "/about":

            self.show_about()

            return

        # ----------------------------------------------------
        # Time
        # ----------------------------------------------------

        if command == "/time":

            current_time = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            self.write(
                f"\nCurrent time: {current_time}\n\n",
                "#AAAAAA"
            )

            return

        # ----------------------------------------------------
        # Normal message
        # ----------------------------------------------------

        self.send_to_backend(user_input)

    # ========================================================
    # FastAPI Request
    # ========================================================

    def send_to_backend(self, message):

        self.write(
            "\nAssistant> ",
            "#00FF66"
        )

        self.write(
            "Thinking...\n",
            "#AAAAAA"
        )

        thread = threading.Thread(
            target=self._backend_request,
            args=(message,),
            daemon=True
        )

        thread.start()

    # ========================================================
    # Backend Request Worker
    # ========================================================

    def _backend_request(self, message):

        payload = {
            "message": message
        }

        try:

            response = requests.post(
                f"{API_BASE_URL}/agent/run",
                json=payload,
                timeout=600
            )

            response.raise_for_status()

            data = response.json()

            assistant_response = data.get(
                "response",
                "The backend returned no response."
            )

            self.root.after(
                0,
                self.display_backend_response,
                assistant_response
            )

        except requests.exceptions.ConnectionError:

            self.root.after(
                0,
                self.display_backend_error,
                "Could not connect to FastAPI.\n"
                f"Make sure the backend is running at:\n"
                f"{API_BASE_URL}"
            )

        except requests.exceptions.Timeout:

            self.root.after(
                0,
                self.display_backend_error,
                "The AI agent took too long to respond."
            )

        except requests.exceptions.HTTPError as exc:

            try:
                error_data = response.json()
                detail = error_data.get(
                    "detail",
                    str(exc)
                )
            except Exception:
                detail = str(exc)

            self.root.after(
                0,
                self.display_backend_error,
                f"Backend error: {detail}"
            )

        except Exception as exc:

            self.root.after(
                0,
                self.display_backend_error,
                f"Unexpected error: {exc}"
            )

    # ========================================================
    # Display Backend Response
    # ========================================================

    def display_backend_response(self, response):

        self.write(
            f"{response}\n\n",
            "#FFFFFF"
        )

    # ========================================================
    # Display Backend Error
    # ========================================================

    def display_backend_error(self, message):

        self.write(
            f"{message}\n\n",
            "#FF5555"
        )

    # ========================================================
    # Help
    # ========================================================

    def show_help(self):

        self.write(
            "\n"
            "Available commands:\n"
            "\n"
            "  /help       Show this help message\n"
            "  /clear      Clear the terminal\n"
            "  /history    Show command history\n"
            "  /about      Show assistant information\n"
            "  /time       Show current time\n"
            "  /exit       Exit the assistant\n"
            "\n",
            "#AAAAAA"
        )

    # ========================================================
    # About
    # ========================================================

    def show_about(self):

        self.write(
            "\n"
            "CLI AI Assistant\n"
            "----------------\n"
            "Version: 0.1.0\n"
            "Interface: Python Tkinter\n"
            "Backend: FastAPI\n"
            "LLM: ollama Face\n"
            "Agent: API Connected\n"
            "\n",
            "#AAAAAA"
        )

    # ========================================================
    # History
    # ========================================================

    def show_history(self):

        if not self.history:

            self.write(
                "\nNo command history.\n\n",
                "#AAAAAA"
            )

            return

        self.write(
            "\nCommand history:\n\n",
            "#AAAAAA"
        )

        for index, command in enumerate(
            self.history,
            start=1
        ):

            self.write(
                f"  {index}. {command}\n",
                "#AAAAAA"
            )

        self.write("\n")

    # ========================================================
    # Clear
    # ========================================================

    def clear_screen(self):

        self.output.configure(
            state="normal"
        )

        self.output.delete(
            "1.0",
            "end"
        )

        self.output.configure(
            state="disabled"
        )

        self.print_startup()

    # ========================================================
    # Ctrl + L
    # ========================================================

    def handle_clear(self, event=None):

        self.clear_screen()

        return "break"

    # ========================================================
    # Escape
    # ========================================================

    def handle_exit(self, event=None):

        self.root.destroy()

        return "break"


# ============================================================
# Application Entry Point
# ============================================================

def main():

    root = tk.Tk()

    app = TerminalApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()


