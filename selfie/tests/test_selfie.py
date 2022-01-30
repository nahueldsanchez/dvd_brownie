from scripts.deploy import scenario_setup, TOKENS_IN_POOL
from scripts.exploit import exploit
from brownie import accounts, AttackerContract


def test_solution():
    token_contract, governance_contract, pool_contract = scenario_setup()
    attacker_contract = AttackerContract.deploy(
        pool_contract, governance_contract, {"from": accounts[2]}
    )

    # Solution goes here
    # Write your exploit
    # :) Good luck
    exploit(attacker_contract)

    # ** SUCCESS CONDITIONS **
    # Attacker has taken all tokens from the pool
    # assert token_contract.balanceOf(attacker_account) == TOKENS_IN_POOL
    assert token_contract.balanceOf(attacker_contract) == TOKENS_IN_POOL
    assert token_contract.balanceOf(pool_contract) == 0
