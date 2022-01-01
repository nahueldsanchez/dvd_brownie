from brownie import TrusterLenderPool, DamnValuableToken, accounts

TOKENS_IN_POOL = '1000000 ether'

def scenario_setup():
    damn_valuable_token = DamnValuableToken.deploy({'from':accounts[0]})
    truster_lender_pool = TrusterLenderPool.deploy(damn_valuable_token.address, {'from':accounts[0]})
    damn_valuable_token.transfer(truster_lender_pool.address, TOKENS_IN_POOL, {'from':accounts[0]})


    return damn_valuable_token, truster_lender_pool