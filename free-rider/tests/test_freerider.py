from brownie import DamnValuableNFT
from scripts.deploy import (AMOUNT_OF_NFTS, BUYER_PAYOUT,
                            MARKETPLACE_INITIAL_ETH_BALANCE, scenario_setup)
from scripts.exploit import exploit


def test_solution():

    pair, market, nft, weth, attacker, buyer = scenario_setup()
    # Solution goes here
    # Write your exploit
    # The exploit must return the contract deployed for the buyer
    # I.E: buyer_contract = exploit(args)
    # :) Good lock
    buyer_contract = exploit(pair, weth, market, nft, attacker, buyer)

    # Asserts, don't change anything starting here
    # Attacker must have earned all ETH from the payout
    assert attacker.balance() > BUYER_PAYOUT
    assert buyer_contract.balance() == 0

    # The buyer extracts all NFTs from its associated contract
    for token in range(AMOUNT_OF_NFTS):
        dvnft = DamnValuableNFT.at(nft)
        tx = dvnft.transferFrom(buyer_contract, buyer, token, {'from': buyer})
        assert dvnft.ownerOf(token) == buyer

    # Exchange must have lost NFTs and ETH
    assert market.amountOfOffers() == 0
    assert market.balance() < MARKETPLACE_INITIAL_ETH_BALANCE
