from brownie import SideEntranceLenderPool, accounts

TOKENS_IN_POOL = '100 ether'


def scenario_setup():
    side_entrance_lender_pool = SideEntranceLenderPool.deploy({'from':accounts[0]})
    side_entrance_lender_pool.deposit({'from':accounts[0], 'value': TOKENS_IN_POOL})

    return side_entrance_lender_pool