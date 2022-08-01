from brownie import FlashLoanReceiver, NaiveReceiverLenderPool
from scripts.deploy import ETHER_IN_POOL, ETHER_IN_RECEIVER, scenario_setup
from scripts.exploit import exploit_multiple_calls, exploit_one_call
from web3 import Web3

FIXED_FEE = '1 ether'


def test_scenario_setup():
    naive_pool, naive_receiver = scenario_setup()

    assert naive_pool.balance() == Web3.toWei(ETHER_IN_POOL, 'ether')
    assert naive_pool.fixedFee() == FIXED_FEE
    assert naive_receiver.balance() == Web3.toWei(ETHER_IN_RECEIVER, 'ether')

def test_solution():
    naive_pool, naive_receiver = scenario_setup()
    # Solution goes here
    # Write your exploit
    # :) Good lock
    #exploit_multiple_calls(naive_pool, naive_receiver)
    exploit_one_call(naive_pool, naive_receiver)
    print(f'naive receiver balance: {naive_receiver.balance()}')
    assert naive_receiver.balance() == 0
    assert naive_pool.balance() == Web3.toWei(ETHER_IN_RECEIVER, 'ether') + \
        Web3.toWei(ETHER_IN_POOL, 'ether')
