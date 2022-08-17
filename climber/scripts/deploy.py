from brownie import accounts, Contract, ClimberTimelock, ClimberVault, DamnValuableToken, ERC1967Proxy, ZERO_ADDRESS
from web3 import Web3

VAULT_TOKEN_BALANCE = '10000000 ether'


def scenario_setup():

    ATTACKER_ACCOUNT = accounts.add()
    PROPOSER_ACCOUNT = accounts.add()
    SWEEPER_ACCOUNT = accounts.add()

    accounts[0].transfer(ATTACKER_ACCOUNT, '0.1 ether')

    assert ATTACKER_ACCOUNT.balance() == '0.1 ether'

    climber_vault_implementation = ClimberVault.deploy({'from': accounts[0]})
    climber_vault_data = climber_vault_implementation.initialize.encode_input(
        accounts[0], PROPOSER_ACCOUNT, SWEEPER_ACCOUNT)
    climber_vault_proxy = ERC1967Proxy.deploy(
        climber_vault_implementation, climber_vault_data, {'from': accounts[0]})

    climber_vault = Contract.from_abi(
        "Climber", climber_vault_proxy, ClimberVault.abi)

    assert climber_vault.getSweeper() == SWEEPER_ACCOUNT
    assert climber_vault.getLastWithdrawalTimestamp() > 0
    assert climber_vault.owner() != ZERO_ADDRESS
    assert climber_vault.owner() != accounts[0]

    time_lock_address = climber_vault.owner()
    time_lock = ClimberTimelock.at(time_lock_address)

    assert time_lock.hasRole(time_lock.PROPOSER_ROLE(),
                             PROPOSER_ACCOUNT) == True
    assert time_lock.hasRole(time_lock.ADMIN_ROLE(), accounts[0]) == True

    damn_valuable_token = DamnValuableToken.deploy({'from': accounts[0]})
    damn_valuable_token.initialize(
        "DamnValuableToken", "DVT", 10 * VAULT_TOKEN_BALANCE)
    damn_valuable_token.transfer(climber_vault, VAULT_TOKEN_BALANCE)

    return time_lock, climber_vault, ATTACKER_ACCOUNT, damn_valuable_token

    # https://docs.openzeppelin.com/contracts/3.x/access-control
