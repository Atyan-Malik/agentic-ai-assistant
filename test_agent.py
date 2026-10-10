
from agent import Agent

agent = Agent()

session_id = None

while True:
    try:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in {"exit", "quit"}:
            print("Agent: Goodbye!")
            break

        if not user_input:
            continue

        result = agent.run(
            message=user_input,
            session_id=session_id,
        )

        session_id = result.session_id
        print(f"\nAgent: {result.response}")

        if not result.success:
            print(f"Error: {result.error}")

    except KeyboardInterrupt:
        print("\nAgent: Goodbye!")
        break
