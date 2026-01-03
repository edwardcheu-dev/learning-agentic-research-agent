"""Tests for main entry point and CLI argument parsing."""

from unittest.mock import Mock, patch

from src.main import parse_args, run_repl, run_tui


class TestCLIArguments:
    """Test command-line argument parsing."""

    def test_default_launches_tui(self):
        """Test that no arguments defaults to TUI mode."""
        args = parse_args([])
        assert args.mode == "tui"

    def test_tui_flag_launches_tui(self):
        """Test that --tui flag launches TUI mode."""
        args = parse_args(["--tui"])
        assert args.mode == "tui"

    def test_repl_flag_launches_repl(self):
        """Test that --repl flag launches REPL mode."""
        args = parse_args(["--repl"])
        assert args.mode == "repl"


class TestRunREPL:
    """Test the run_repl function."""

    @patch("src.main.create_client")
    @patch("src.main.Agent")
    @patch("builtins.input", side_effect=["quit"])
    @patch("builtins.print")
    def test_run_repl_creates_agent_and_runs_loop(
        self, mock_print, mock_input, mock_agent_class, mock_create_client
    ):
        """Test that run_repl creates agent and runs REPL loop."""
        # Mock client and agent
        mock_client = Mock()
        mock_create_client.return_value = mock_client
        mock_agent = Mock()
        mock_agent_class.return_value = mock_agent

        # Run REPL
        run_repl()

        # Verify client was created
        mock_create_client.assert_called_once()

        # Verify agent was created with client
        mock_agent_class.assert_called_once()
        assert mock_agent_class.call_args[1]["client"] == mock_client


class TestRunTUI:
    """Test the run_tui function."""

    @patch("src.main.ResearchAssistantApp")
    def test_run_tui_creates_and_runs_app(self, mock_app_class):
        """Test that run_tui creates and runs the Textual app."""
        # Mock app
        mock_app = Mock()
        mock_app_class.return_value = mock_app

        # Run TUI
        run_tui()

        # Verify app was created and run
        mock_app_class.assert_called_once()
        mock_app.run.assert_called_once()
