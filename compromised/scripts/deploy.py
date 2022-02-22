from brownie import (DamnValuableNFT, Exchange, TrustfulOracle,
                     TrustfulOracleInitializer, accounts)
from web3 import Web3

EXCHANGE_INITIAL_ETH_BALANCE = Web3.toWei(
    99, 'ether'
)  # Changed these values due to Brownie's accounts default balance
INITIAL_NFT_PRICE = Web3.toWei(9, 'ether')
TRUSTED_SOURCES = [
    '0xA73209FB1a42495120166736362A1DfA9F95A105',
    '0xe92401A4d3af5E446d93D11EEc806b1462b39D15',
    '0x81A5D6E50C214044bE44cA0CB057fe119097850c',
]


def scenario_setup():

    # Accounts[0] used for deployment
    trustful_oracle_initializer = TrustfulOracleInitializer.deploy(
        TRUSTED_SOURCES,
        ['DVNFT', 'DVNFT', 'DVNFT'],
        [INITIAL_NFT_PRICE, INITIAL_NFT_PRICE, INITIAL_NFT_PRICE],
        {'from': accounts[0]},
    )
    trustful_oracle = TrustfulOracle.at(trustful_oracle_initializer.oracle())
    exchange = Exchange.deploy(
        trustful_oracle, {'from': accounts[0], 'value': EXCHANGE_INITIAL_ETH_BALANCE}
    )
    assert exchange.balance() == EXCHANGE_INITIAL_ETH_BALANCE
    nft_token = DamnValuableNFT.at(exchange.token())

    return trustful_oracle, exchange, nft_token
