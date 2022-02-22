from scripts.deploy import (
    EXCHANGE_INITIAL_ETH_BALANCE,
    INITIAL_NFT_PRICE,
    accounts,
    scenario_setup,
)
from scripts.exploit import exploit


def test_solution():
    trusted_oracle, exchange, nft = scenario_setup()
    ATTACKER_ACCOUNT = accounts[9]
    ATTACKER_INITIAL_BALANCE = ATTACKER_ACCOUNT.balance()

    # Solution goes here
    # Write your exploit
    # :) Good lock
    exploit(trusted_oracle, exchange, nft, ATTACKER_ACCOUNT)

    # Asserts, don't change anything starting here
    assert exchange.balance() == 0
    assert (
        ATTACKER_ACCOUNT.balance()
        == EXCHANGE_INITIAL_ETH_BALANCE + ATTACKER_INITIAL_BALANCE
    )
    assert nft.balanceOf(ATTACKER_ACCOUNT) == 0
    assert trusted_oracle.getMedianPrice('DVNFT') == INITIAL_NFT_PRICE
