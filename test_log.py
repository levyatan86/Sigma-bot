from sheets_integration import log_trade_to_sheet

log_trade_to_sheet(
    pair="TEST/USDT",
    direction="long",
    entry=1234.5,
    sl=1200,
    tp1=1300,
    tp2=1350,
    session="Test",
    notes="manual test",
    emotion="neutral",
    score="5.0"
)
