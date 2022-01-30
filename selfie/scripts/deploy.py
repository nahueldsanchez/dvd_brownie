from brownie import accounts, DamnValuableTokenSnapshot, SimpleGovernance, SelfiePool

TOKEN_INITIAL_SUPPLY = "2000000 ether"
TOKENS_IN_POOL = "1500000 ether"


def scenario_setup():
    token_contract = DamnValuableTokenSnapshot.deploy(
        TOKEN_INITIAL_SUPPLY, {"from": accounts[0]}
    )
    governance_contract = SimpleGovernance.deploy(token_contract, {"from": accounts[0]})
    pool_contract = SelfiePool.deploy(
        token_contract, governance_contract, {"from": accounts[0]}
    )

    print(
        f"Damn Valuable Token Snapshot contract deployed at: {token_contract.address}"
    )
    print(f"Governance Token deployed at: {governance_contract.address}")
    print(f"Selfie Pool deployed at: {pool_contract.address}")

    token_contract.transfer(pool_contract, TOKENS_IN_POOL)

    assert token_contract.balanceOf(pool_contract) == TOKENS_IN_POOL

    return token_contract, governance_contract, pool_contract
