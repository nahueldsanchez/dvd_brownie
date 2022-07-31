import json

from brownie import (WETH9, Contract, DamnValuableNFT, DamnValuableToken,
                     FreeRiderBuyer, FreeRiderNFTMarketplace, accounts, chain)
from web3 import Web3

RANDOM_ADDRESS = '0x5832727e34162736F3e7082EDad9DCfD76e15D0a'
RANDOM_ADDRESS_PK = '57f7f022e5941d0573114e2aab6e08aeb9a6f28b42d48e63a374783d7f1fdadb'

ATTACKER_INITIAL_ETH_BALANCE = Web3.toWei(0.5, 'ether')

NFT_PRICE = Web3.toWei(15, 'ether')
AMOUNT_OF_NFTS = 6
MARKETPLACE_INITIAL_ETH_BALANCE = Web3.toWei(90, 'ether')
BUYER_PAYOUT = Web3.toWei(45, 'ether')
UNISWAP_INITIAL_TOKEN_RESERVE = Web3.toWei(15000, 'ether')
UNISWAP_INITIAL_WETH_RESERVE = Web3.toWei(9000, 'ether')


def load_json(json_file):
    with open(f'./build-uniswap-v2/{json_file}', 'r') as f:
        contract_metadata = json.loads(f.read())
        contract_abi = contract_metadata['abi']
        contract_bytecode = contract_metadata['bytecode']
    return contract_abi, contract_bytecode


def deploy_bytecode(contract_abi, contract_bytecode, *args):

    # This will connect to Brownie's ganache instance
    w3_client = Web3(Web3.HTTPProvider('http://0.0.0.0:8545'))

    temp_contract = w3_client.eth.contract(
        abi=contract_abi, bytecode=contract_bytecode)
    n = w3_client.eth.get_transaction_count(RANDOM_ADDRESS)

    tx = temp_contract.constructor(*args).buildTransaction(
        {'from': RANDOM_ADDRESS, 'nonce': n, 'gasPrice': w3_client.eth.gas_price}
    )
    signed_tx = w3_client.eth.account.sign_transaction(
        tx, private_key=RANDOM_ADDRESS_PK)

    accounts[0].transfer(RANDOM_ADDRESS, '1 ether')
    txh = w3_client.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = w3_client.eth.wait_for_transaction_receipt(txh)

    return tx_receipt.contractAddress


def scenario_setup():

    # Set attacker account
    ATTACKER_ACCOUNT = accounts.add()
    accounts[1].transfer(ATTACKER_ACCOUNT, '0.5 ether')
    assert ATTACKER_ACCOUNT.balance() == ATTACKER_INITIAL_ETH_BALANCE
    # ####################

    # Set buyer account
    BUYER_ACCOUNT = accounts.add()
    accounts[1].transfer(BUYER_ACCOUNT, '50 ether')

    # Deploy DVT and WETH9
    damn_valuable_token = DamnValuableToken.deploy({'from': accounts[0]})
    weth9 = WETH9.deploy({'from': accounts[0]})
    # ####################

    # Deploy UNISWAP V2 Factory
    uniswap_v2_factory_abi, uniswap_v2_factory_bytecode = load_json(
        'UniswapV2Factory.json')
    uniswap_v2_factory_address = deploy_bytecode(
        uniswap_v2_factory_abi, uniswap_v2_factory_bytecode, '0x0000000000000000000000000000000000000000'
    )
    uniswap_v2_factory = Contract.from_abi(
        'UniswapV2Factory', uniswap_v2_factory_address, uniswap_v2_factory_abi
    )
    ###########################

    # Deploy UNISWAP V2 Router
    uniswap_v2_router_abi, uniswap_v2_router_bytecode = load_json(
        'UniswapV2Router02.json')
    uniswap_v2_router_address = deploy_bytecode(
        uniswap_v2_router_abi, uniswap_v2_router_bytecode, uniswap_v2_factory.address, weth9.address)
    uniswap_v2_router = Contract.from_abi(
        'UniswapV2Router', uniswap_v2_router_address, uniswap_v2_router_abi)
    #############################

    damn_valuable_token.approve(
        uniswap_v2_router, UNISWAP_INITIAL_TOKEN_RESERVE, {'from': accounts[0]})
    deadline = chain[-1].timestamp * 2
    tx = uniswap_v2_router.addLiquidityETH(damn_valuable_token.address, UNISWAP_INITIAL_TOKEN_RESERVE, 0, 0, RANDOM_ADDRESS, deadline, {
                                           'from': accounts[0], 'value': UNISWAP_INITIAL_WETH_RESERVE})

    # Deploy UNISWAP v2 Pair
    uniswap_v2_pair_abi, uniswap_v2_pair_bytecode = load_json(
        'UniswapV2Pair.json')
    uniswap_v2_pair = Contract.from_abi(
        'UniswapV2Pair', uniswap_v2_factory.getPair(
            weth9, damn_valuable_token), uniswap_v2_pair_abi
    )
    ########################

    assert uniswap_v2_pair.token0() == damn_valuable_token
    assert uniswap_v2_pair.token1() == weth9
    assert uniswap_v2_pair.balanceOf(RANDOM_ADDRESS) > 0

    marketplace = FreeRiderNFTMarketplace.deploy(
        AMOUNT_OF_NFTS, {'from': accounts[0], 'value': MARKETPLACE_INITIAL_ETH_BALANCE})
    nft = DamnValuableNFT.at(marketplace.token())

    for id in range(AMOUNT_OF_NFTS):
        assert nft.ownerOf(id) == accounts[0]

    nft.setApprovalForAll(marketplace, True, {'from': accounts[0]})

    marketplace.offerMany([x for x in range(6)], [
                          NFT_PRICE for _ in range(6)], {'from': accounts[0]})
    assert marketplace.amountOfOffers() == 6

    return uniswap_v2_pair, marketplace, nft, weth9, ATTACKER_ACCOUNT, BUYER_ACCOUNT


def setup_buyer_contract(partner_address, nft_address, buyer_account):
    buyer_contract = FreeRiderBuyer.deploy(partner_address, nft_address, {
                                           'from': buyer_account, 'value': BUYER_PAYOUT})

    return buyer_contract
