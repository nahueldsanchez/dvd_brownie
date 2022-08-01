import brownie
from scripts.deployer import (INITIAL_ATTACKER_TOKEN_BALANCE, TOKENS_IN_POOL,
                              scenario_setup)
from scripts.exploit import exploit


def test_scenario_setup(accounts):
    # Arrange/Act
    unstoppable_pool, damn_valuable_token = scenario_setup()

    # Assert
    # accounts[1] will be the attacker's account
    assert damn_valuable_token.balanceOf(
        unstoppable_pool.address) == TOKENS_IN_POOL
    assert damn_valuable_token.balanceOf(
        accounts[1]) == INITIAL_ATTACKER_TOKEN_BALANCE


def test_unstoppable_pool_flashloans_work(accounts):
    unstoppable_pool, _ = scenario_setup()
    receiver_unstoppable = brownie.ReceiverUnstoppable.deploy(
        unstoppable_pool.address, {'from': accounts[0]})
    tx = receiver_unstoppable.executeFlashLoan(10)
    assert tx


def test_solution(accounts):
    unstoppable_pool, damn_valuable_token = scenario_setup()
    receiver_unstoppable = brownie.ReceiverUnstoppable.deploy(
        unstoppable_pool.address, {'from': accounts[0]})
    
    attacker = accounts[1]

    # Solution goes here
    # Write your exploit
    # :) Good lock
    exploit(unstoppable_pool, attacker, damn_valuable_token)

    with brownie.reverts():
        receiver_unstoppable.executeFlashLoan(10)
