"""Historical console-selection testimony from the compatibility CLI."""

from scripts import seed_local


def test_console_options_alone_selected_the_compatibility_console():
    assert seed_local._is_console_invocation(["--db", "x"])


def test_other_arguments_selected_the_compatibility_dispatcher():
    assert not seed_local._is_console_invocation(["--show-inference-catalog"])


def test_the_compatibility_session_argument_used_its_historical_default():
    args = seed_local.build_parser().parse_args([])
    assert args.session == seed_local.DEFAULT_SESSION
