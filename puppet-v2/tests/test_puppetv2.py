from scripts.deploy import (
    scenario_setup,
    ATTACKER_INITIAL_TOKEN_BALANCE,
    POOL_INITIAL_TOKEN_BALANCE,
    POOL_INITIAL_TOKEN_BALANCE,
)
from brownie import chain
from scripts.exploit import exploit


def test_solution():
    routerv2, dvt, weth, lending_pool, attacker_account = scenario_setup()

    # Solution goes here
    # Write your exploit
    # :) Good lock
    exploit(routerv2, lending_pool, attacker_account, dvt, weth)

    # Asserts, don't change anything starting here
    assert dvt.balanceOf(lending_pool) == 0
    assert dvt.balanceOf(attacker_account) > POOL_INITIAL_TOKEN_BALANCE
