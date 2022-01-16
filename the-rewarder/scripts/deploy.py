from brownie import (AccountingToken, DamnValuableToken, FlashLoanerPool,
                     RewardToken, TheRewarderPool, accounts, chain)
from brownie.network import rpc
from web3 import Web3

TOKENS_IN_LENDER_POOL = "1000000 ether"


def scenario_setup():
    liquidity_token = DamnValuableToken.deploy({"from": accounts[0]})
    flash_loan_pool = FlashLoanerPool.deploy(liquidity_token, {"from": accounts[0]})

    liquidity_token.transfer(flash_loan_pool, TOKENS_IN_LENDER_POOL)

    rewarder_pool = TheRewarderPool.deploy(liquidity_token, {"from": accounts[0]})
    reward_token = RewardToken.at(rewarder_pool.rewardToken())
    accounting_token = AccountingToken.at(rewarder_pool.accToken())

    # Alice, Bob, Charlie and David deposit 100 tokens each
    for i in range(5, 9):
        amount = "100 ether"
        print(f"Transfering liquidity tokens to account: {i}")
        tx = liquidity_token.transfer(accounts[i], amount, {"from": accounts[0]})
        tx.wait(1)
        tx = liquidity_token.approve(rewarder_pool, amount, {"from": accounts[i]})
        tx.wait(1)
        rewarder_pool.deposit(amount, {"from": accounts[i]})

        assert accounting_token.balanceOf(accounts[i]) == amount

    assert accounting_token.totalSupply() == Web3.toWei(400, "ether")
    assert reward_token.totalSupply() == 0

    # Advancing five days
    chain.sleep(60 * 60 * 24 * 5)

    # Each depositor gets 25 reward tokens
    for i in range(5, 9):
        rewarder_pool.distributeRewards({"from": accounts[i]})
        assert reward_token.balanceOf(accounts[i]) == Web3.toWei(25, "ether")

    assert reward_token.totalSupply() == Web3.toWei(100, "ether")

    # Attacker starts with zero DVT tokens in balance
    # assert liquidity_token.balanceOf(attacker_address) == 0

    # Two rounds should have occurred so far
    assert rewarder_pool.roundNumber() == 2

    return (
        liquidity_token,
        flash_loan_pool,
        rewarder_pool,
        reward_token,
    )
