from brownie import DamnValuableToken, WalletRegistry, accounts, project
from web3 import Web3

# Changes needed to make this work:
# packages/safe-global/safe-contracts@1.3.0-libs.0/contracts/interfaces/ViewStorageAccessible.sol comment out solidity pragma
# packages/safe-global/safe-contracts@1.3.0-libs.0/contracts/test/ERC20Token.sol comment out solidity pragma
# Download https://github.com/gnosis/mock-contract/tree/master and save it into packages/safe-global/safe-contracts@1.3.0-libs.0/

AMOUNT_TOKENS_DISTRIBUTED = Web3.toWei(40, 'ether')


def scenario_setup():

    ATTACKER_ACCOUNT = accounts.add()
    ALICE = accounts.add()
    BOB = accounts.add()
    CHARLIE = accounts.add()
    DAVID = accounts.add()

    users = [ALICE, BOB, CHARLIE, DAVID]

    gnosis_project = project.load(
        'safe-global/safe-contracts@1.3.0-libs.0', name='GnosisSafe')
    master_copy = gnosis_project.GnosisSafe.deploy({'from': accounts[0]})
    wallet_factory = gnosis_project.GnosisSafeProxyFactory.deploy(
        {'from': accounts[0]})
    token = DamnValuableToken.deploy({'from': accounts[0]})

    wallet_registry = WalletRegistry.deploy(
        master_copy, wallet_factory, token, users, {'from': accounts[0]})

    for user in users:
        assert wallet_registry.beneficiaries(user) == True

    token.transfer(wallet_registry, AMOUNT_TOKENS_DISTRIBUTED,
                   {'from': accounts[0]})

    return master_copy, wallet_registry, wallet_factory, token, ATTACKER_ACCOUNT, ALICE, BOB, CHARLIE, DAVID
