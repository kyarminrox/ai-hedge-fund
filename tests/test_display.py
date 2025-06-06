import os
import sys
import types

# Provide minimal stubs if dependencies aren't installed
try:
    import colorama  # noqa: F401
except ImportError:  # pragma: no cover
    stub = types.SimpleNamespace(
        Fore=types.SimpleNamespace(WHITE="", CYAN="", GREEN="", RED="", BLUE="", YELLOW=""),
        Style=types.SimpleNamespace(BRIGHT="", RESET_ALL=""),
    )
    sys.modules['colorama'] = stub

try:
    from tabulate import tabulate  # noqa: F401
except ImportError:  # pragma: no cover
    tabulate_module = types.ModuleType('tabulate')
    def dummy_tabulate(*args, **kwargs):
        return ""
    tabulate_module.tabulate = dummy_tabulate
    sys.modules['tabulate'] = tabulate_module

# Ensure src is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

# Stub utils.analysts to avoid heavy imports when importing utils.display
analysts_stub = types.ModuleType('utils.analysts')
analysts_stub.ANALYST_ORDER = []
sys.modules.setdefault('utils.analysts', analysts_stub)

from utils.display import format_backtest_row


def test_format_backtest_row_summary():
    row = format_backtest_row(
        date="2024-01-01",
        ticker="",
        action="",
        quantity=0,
        price=0,
        shares_owned=0,
        position_value=0,
        bullish_count=0,
        bearish_count=0,
        neutral_count=0,
        is_summary=True,
        total_value=123456.78,
        return_pct=5.42,
        cash_balance=23456.78,
        total_position_value=100000.00,
        sharpe_ratio=1.23,
        sortino_ratio=1.11,
        max_drawdown=7.89,
    )

    # Expect 13 columns in summary rows
    assert len(row) == 13

    # Check that formatted monetary values and return are present
    assert "100,000.00" in row[6]
    assert "23,456.78" in row[7]
    assert "123,456.78" in row[8]
    assert "+5.42%" in row[9]
    assert "PORTFOLIO SUMMARY" in row[1]

