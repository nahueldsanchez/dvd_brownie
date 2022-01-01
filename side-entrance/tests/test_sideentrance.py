from scripts.deploy import TOKENS_IN_POOL, accounts, scenario_setup
from brownie import AttackerContract
import pytest

@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass

def test_scenario_setup():
    side_entrance_lender_pool = scenario_setup()

    assert side_entrance_lender_pool.balance() == TOKENS_IN_POOL


def test_solution():
    side_entrance_lender_pool = scenario_setup()
    
    # Solution goes here
    # Write your exploit
    # :) Good lock
    # Attacker is using attacker_contract to launch the attack
    attacker_contract = AttackerContract.deploy({'from':accounts[1]})
    attacker_initial_balance = attacker_contract.balance()
    attacker_contract.exploit(side_entrance_lender_pool, TOKENS_IN_POOL)

    assert side_entrance_lender_pool.balance() == 0
    assert attacker_contract.balance() > attacker_initial_balance
