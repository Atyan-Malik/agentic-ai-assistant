from ollama import AsyncClient


MODEL = "qwen2.5:latest"

client = AsyncClient(
    host="http://127.0.0.1:11434"
)


async def generate_response(message: str) -> str:
    response = await client.chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an intelligent AI assistant. "
                    "Give clear, accurate, and useful answers. "
                    "Use simple explanations when appropriate."
                ),
            },
            {
                "role": "user",
                "content": message,
            },
        ],
    )

    return response["message"]["content"]