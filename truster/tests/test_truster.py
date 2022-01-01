from scripts.deploy import TOKENS_IN_POOL, accounts, scenario_setup
from scripts.exploit import exploit_multiple_txs, exploit_one_tx


def test_scenario_setup():
    damn_valuable_token, truster_lender_pool = scenario_setup()

    assert damn_valuable_token.balanceOf(truster_lender_pool) == TOKENS_IN_POOL
    assert damn_valuable_token.balanceOf(accounts[1]) == 0


def test_solution():
    damn_valuable_token, truster_lender_pool = scenario_setup()
    # Solution goes here
    # Write your exploit
    # :) Good lock
    # Attacker is using accounts[1]
    #exploit_multiple_txs(truster_lender_pool, damn_valuable_token, accounts[1])
    exploit_one_tx(damn_valuable_token, truster_lender_pool,
                   accounts[1], TOKENS_IN_POOL)
    assert damn_valuable_token.balanceOf(accounts[1]) == TOKENS_IN_POOL
    assert damn_valuable_token.balanceOf(truster_lender_pool) == 0
