"""
Interactive interface for the Research Assistant agent.

This is the main entry point for running the agent interactively.
Supports both TUI (default) and REPL modes.
Users can ask questions and see the ReAct reasoning process in action.
"""

import argparse

from src.agents.agent import Agent
from src.client import create_client
from src.config import DEFAULT_MAX_ITERATIONS
from src.tui.app import ResearchAssistantApp


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments.

    Args:
        args: List of arguments to parse (for testing). If None, uses sys.argv.

    Returns:
        Parsed arguments with mode attribute.
    """
    parser = argparse.ArgumentParser(
        description="Research Assistant - Multi-agent AI system"
    )
    parser.add_argument(
        "--tui",
        action="store_const",
        const="tui",
        dest="mode",
        help="Launch the Textual TUI interface (default)",
    )
    parser.add_argument(
        "--repl",
        action="store_const",
        const="repl",
        dest="mode",
        help="Launch the classic REPL interface",
    )
    parser.set_defaults(mode="tui")

    return parser.parse_args(args)


def run_repl() -> None:
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
        agent = Agent(client=client, max_iterations=DEFAULT_MAX_ITERATIONS)
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


def run_tui() -> None:
    """Run the Textual TUI interface for the Research Assistant."""
    app = ResearchAssistantApp()
    app.run()


def main() -> None:
    """Main entry point - parse arguments and launch appropriate interface."""
    args = parse_args()

    if args.mode == "repl":
        run_repl()
    else:
        run_tui()


if __name__ == "__main__":
    main()
