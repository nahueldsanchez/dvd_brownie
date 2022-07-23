import json
from decimal import Decimal
from web3 import Web3
from brownie import Contract, accounts, DamnValuableToken, PuppetPool, chain, Wei

RANDOM_ADDRESS = '0x5832727e34162736F3e7082EDad9DCfD76e15D0a'
RANDOM_ADDRESS_PK = '57f7f022e5941d0573114e2aab6e08aeb9a6f28b42d48e63a374783d7f1fdadb'

UNISWAP_INITIAL_TOKEN_RESERVE = Web3.toWei(10, 'ether')
UNISWAP_INITIAL_ETH_RESERVE = Web3.toWei(10, 'ether')

ATTACKER_INITIAL_TOKEN_BALANCE = Web3.toWei(1000, 'ether')
ATTACKER_INITIAL_ETH_BALANCE = Web3.toWei(25, 'ether')
POOL_INITIAL_TOKEN_BALANCE = Web3.toWei(100000, 'ether')


def load_json(json_file):
    with open(f'./build-uniswap-v1/{json_file}', 'r') as f:
        contract_metadata = json.loads(f.read())
        contract_abi = contract_metadata['abi']
        contract_bytecode = contract_metadata['evm']['bytecode']['object']
    return contract_abi, contract_bytecode


def deploy_bytecode(contract_abi, contract_bytecode):

    # This will connect to Brownie's ganache instance
    w3_client = Web3(Web3.HTTPProvider('http://0.0.0.0:8545'))

    temp_contract = w3_client.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
    n = w3_client.eth.get_transaction_count(RANDOM_ADDRESS)
    tx = temp_contract.constructor().buildTransaction(
        {'from': RANDOM_ADDRESS, 'nonce': n, 'gasPrice': w3_client.eth.gas_price}
    )
    signed_tx = w3_client.eth.account.sign_transaction(tx, private_key=RANDOM_ADDRESS_PK)

    accounts[0].transfer(RANDOM_ADDRESS, '1 ether')
    txh = w3_client.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = w3_client.eth.wait_for_transaction_receipt(txh)

    return tx_receipt.contractAddress

# From: https://github.com/wuwe1/damn-vulnerable-defi-brownie/blob/ec115648cc319811ef09519c433bce9772753cd9/tests/test_puppet.py#L48
def calculate_token_to_eth_input_price(token_sold, token_in_reserve, ether_in_reserve):
    token_sold = Decimal(token_sold)
    token_in_reserve = Decimal(token_in_reserve)
    ether_in_reserve = Decimal(ether_in_reserve)
    return Wei(
        token_sold
        * 997
        * ether_in_reserve
        / (token_in_reserve * 1000 + token_sold * 997))



def scenario_setup():

    damn_valuable_token = DamnValuableToken.deploy({'from': accounts[0]})

    uniswap_factory_abi, uniswap_factory_bytecode = load_json('UniswapV1Factory.json')
    uniswap_factory_address = deploy_bytecode(
        uniswap_factory_abi, uniswap_factory_bytecode
    )
    uniswap_factory = Contract.from_abi(
        'UniswapV1Factory', uniswap_factory_address, uniswap_factory_abi
    )

    uniswap_exchange_abi, uniswap_exchange_bytecode = load_json(
        'UniswapV1Exchange.json'
    )
    uniswap_exchange_address = deploy_bytecode(
        uniswap_exchange_abi, uniswap_exchange_bytecode
    )
    uniswap_exchange_template = Contract.from_abi(
        'UniswapV1ExchangeTemplate', uniswap_exchange_address, uniswap_exchange_abi
    )

    uniswap_factory.initializeFactory(uniswap_exchange_template, {'from': accounts[0]})
    tx = uniswap_factory.createExchange(damn_valuable_token, {'from': accounts[0]})

    new_exchange_address = tx.events['NewExchange']['exchange']
    uniswap_exchange = Contract.from_abi(
        'UniswapV1Exchange', new_exchange_address, uniswap_exchange_abi
    )

    lending_pool = PuppetPool.deploy(
        damn_valuable_token, new_exchange_address, {'from': accounts[0]}
    )

    damn_valuable_token.approve(new_exchange_address, UNISWAP_INITIAL_TOKEN_RESERVE)

    deadline = chain[-1].timestamp * 2

    uniswap_exchange.addLiquidity(
        0,
        UNISWAP_INITIAL_TOKEN_RESERVE,
        deadline,
        {'value': UNISWAP_INITIAL_ETH_RESERVE, 'from': accounts[0]},
    )

    assert uniswap_exchange.getTokenToEthInputPrice(
        Web3.toWei(1, 'ether')
    ) == calculate_token_to_eth_input_price(
        Web3.toWei(1, 'ether'),
        UNISWAP_INITIAL_TOKEN_RESERVE,
        UNISWAP_INITIAL_ETH_RESERVE,
    )

    ATTACKER_ACCOUNT = accounts.add()
    accounts[1].transfer(ATTACKER_ACCOUNT, '25 ether')
    assert ATTACKER_ACCOUNT.balance() == ATTACKER_INITIAL_ETH_BALANCE

    damn_valuable_token.transfer(ATTACKER_ACCOUNT, ATTACKER_INITIAL_TOKEN_BALANCE)
    damn_valuable_token.transfer(lending_pool, POOL_INITIAL_TOKEN_BALANCE)

    assert lending_pool.calculateDepositRequired(Web3.toWei(1, 'ether')) == Web3.toWei(2, 'ether')
    assert lending_pool.calculateDepositRequired(POOL_INITIAL_TOKEN_BALANCE) == POOL_INITIAL_TOKEN_BALANCE * 2

    return uniswap_exchange, lending_pool, damn_valuable_token, ATTACKER_ACCOUNT
