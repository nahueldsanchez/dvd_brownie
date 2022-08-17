from scripts.deploy import scenario_setup, VAULT_TOKEN_BALANCE
from scripts.exploit import exploit


def test_solution():
    time_lock, climber_vault, ATTACKER_ACCOUNT, damn_valuable_token = scenario_setup()
    # Solution goes here
    # Write your exploit
    # :) Good lock

    exploit(climber_vault, time_lock, ATTACKER_ACCOUNT, damn_valuable_token)

    # Asserts, don't change anything starting here
    assert damn_valuable_token.balanceOf(climber_vault) == 0
    assert damn_valuable_token.balanceOf(ATTACKER_ACCOUNT) == VAULT_TOKEN_BALANCE