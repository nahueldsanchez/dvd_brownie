from brownie import accounts, chain
from scripts.deploy import TOKENS_IN_LENDER_POOL, scenario_setup
from scripts.exploit import exploit
from web3 import Web3


def test_solution():
    (
        liquidity_token,
        flash_loan_pool,
        rewarder_pool,
        reward_token,
    ) = scenario_setup()

    # Solution goes here
    # Write your exploit
    # :) Good lock
    # Attacker is using attacker_contract to launch the attack
    attacker_contract, attacker_address = exploit(
        liquidity_token, rewarder_pool, flash_loan_pool
    )

    # Let's advance time until the next rewards round
    chain.sleep(60 * 60 * 24 * 5)

    # And just when the round is started launch the attack
    # Attack is being done with the AttackerContract contract
    tx = attacker_contract.attack(TOKENS_IN_LENDER_POOL, {"from": attacker_address})

    # Only one round should have taken place
    assert rewarder_pool.roundNumber() == 3

    # Users should get neglegible rewards this round
    # Alice, Bob, Charlie and David's accounts
    for i in range(5, 9):
        rewarder_pool.distributeRewards({"from": accounts[i]})
        rewards = reward_token.balanceOf(accounts[i]) - Web3.toWei(25, "ether")

        assert rewards < Web3.toWei(0.01, "ether")

    assert reward_token.totalSupply() > Web3.toWei(100, "ether")

    # The amount of rewards earned should be really close to 100 tokens
    attacker_rewards = reward_token.balanceOf(attacker_contract)
    print(attacker_rewards)
    delta = Web3.toWei(100, "ether") - attacker_rewards

    assert delta < Web3.toWei(0.1, "ether")

    # Attacker finishes with zero DVT tokens in balance
    assert liquidity_token.balanceOf(attacker_contract) == 0
