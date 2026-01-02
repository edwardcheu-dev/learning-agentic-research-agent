"""
Interactive REPL for the Research Assistant agent.

This is the main entry point for running the agent interactively.
Users can ask questions and see the ReAct reasoning process in action.
"""

import os
import openai
from src.agents.agent import Agent


def create_client():
    """Create OpenAI client configured for POE API.

    Returns:
        openai.OpenAI: Configured client instance

    Raises:
        ValueError: If POE_API_KEY environment variable is not set
    """
    api_key = os.getenv("POE_API_KEY")
    if not api_key:
        raise ValueError(
            "POE_API_KEY environment variable not set. "
            "Please set it in your shell configuration."
        )

    return openai.OpenAI(
        api_key=api_key,
        base_url="https://api.poe.com/v1",
    )


def main():
    """Run the interactive REPL for the Research Assistant."""
    print("=" * 60)
    print("Research Assistant - Phase 1: Basic Agentic Loop")
    print("=" * 60)
    print("\nThis agent uses ReAct-style reasoning to answer questions.")
    print("You'll see the agent's Thoughts, Actions, and Observations.")
    print("\nAvailable tools:")
    print("  - search_web: Search for information (placeholder)")
    print("  - save_note: Save notes (placeholder)")
    print("\nType 'quit' or 'exit' to stop.\n")

    # Create client and agent
    try:
        client = create_client()
        agent = Agent(client=client, max_iterations=3)
    except ValueError as e:
        print(f"Error: {e}")
        return

    # REPL loop
    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()

            # Check for exit commands
            if user_input.lower() in ["quit", "exit", "q"]:
                print("\nGoodbye!")
                break

            # Skip empty input
            if not user_input:
                continue

            # Run agent
            print("\n" + "-" * 60)
            result = agent.run(user_input)
            print(result)
            print("-" * 60)

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again or type 'quit' to exit.")


if __name__ == "__main__":
    main()
