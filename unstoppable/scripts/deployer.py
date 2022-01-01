from brownie import (DamnValuableToken, UnstoppableLender)
from brownie import accounts

TOKENS_IN_POOL = '1000000 ether'
INITIAL_ATTACKER_TOKEN_BALANCE = '100 ether'


def scenario_setup():
    #ATTACKER = accounts[1]
    damn_valuable_token = DamnValuableToken.deploy({'from': accounts[0]})
    unstoppable_pool = UnstoppableLender.deploy(
        damn_valuable_token.address, {'from': accounts[0]})

    damn_valuable_token.approve(
        unstoppable_pool.address, TOKENS_IN_POOL, {'from': accounts[0]})
    unstoppable_pool.depositTokens(TOKENS_IN_POOL, {'from': accounts[0]})
    damn_valuable_token.transfer(
        accounts[1], INITIAL_ATTACKER_TOKEN_BALANCE)

    return unstoppable_pool, damn_valuable_token
