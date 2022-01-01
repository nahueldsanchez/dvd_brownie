from brownie import FlashLoanReceiver, NaiveReceiverLenderPool, accounts
from web3 import Web3


ETHER_IN_POOL = 99
ETHER_IN_RECEIVER = 10


def scenario_setup():
    naive_receiver_lender_pool = NaiveReceiverLenderPool.deploy(
        {'from': accounts[0]})
    accounts[1].transfer(naive_receiver_lender_pool,
                         Web3.toWei(ETHER_IN_POOL, 'ether'))

    flash_loan_receiver = FlashLoanReceiver.deploy(
        naive_receiver_lender_pool, {'from': accounts[0]})
    accounts[2].transfer(flash_loan_receiver,
                         Web3.toWei(ETHER_IN_RECEIVER, 'ether'))

    return naive_receiver_lender_pool, flash_loan_receiver
