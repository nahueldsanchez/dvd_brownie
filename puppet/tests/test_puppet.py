from scripts.deploy import (
    scenario_setup,
    ATTACKER_INITIAL_TOKEN_BALANCE,
    POOL_INITIAL_TOKEN_BALANCE,
    POOL_INITIAL_TOKEN_BALANCE,
)
from brownie import chain
from scripts.exploit import exploit


def test_solution():
    exchange, lending_pool, token, attacker_account = scenario_setup()

    # Solution goes here
    # Write your exploit
    # :) Good lock
    exploit(exchange, lending_pool, attacker_account, token)

    # Asserts, don't change anything starting here
    assert token.balanceOf(lending_pool) == 0
    assert token.balanceOf(attacker_account) > POOL_INITIAL_TOKEN_BALANCE
