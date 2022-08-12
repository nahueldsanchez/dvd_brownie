from scripts.deploy import AMOUNT_TOKENS_DISTRIBUTED, scenario_setup
from scripts.exploit import exploit
from brownie import ZERO_ADDRESS


def test_solution():
    master_copy, wallet_registry, wallet_factory, dvt, attacker, alice, bob, charlie, david = scenario_setup()
    victims = [alice, bob, charlie, david]
    # Solution goes here
    # Write your exploit
    # :) Good lock
    
    exploit(victims, wallet_factory, wallet_registry, master_copy, dvt, attacker)

    # Asserts, don't change anything starting here
    # User must have registered a wallet
    for user in victims:
        assert wallet_registry.wallets(user) != ZERO_ADDRESS
    
    # User is no longer registered as a beneficiary
    for user in victims:
        assert wallet_registry.beneficiaries(user) == False

    # Attacker must have taken all tokens
    assert dvt.balanceOf(attacker) == AMOUNT_TOKENS_DISTRIBUTED
