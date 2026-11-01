from crypto_bot.paper_executor import check_exit_conditions

def test_check_exit_conditions():
    t={"stop_loss":90,"take_profit":110}
    assert check_exit_conditions(t, 89)=="STOP"
    assert check_exit_conditions(t, 111)=="TARGET"
    assert check_exit_conditions(t, 100) is None
