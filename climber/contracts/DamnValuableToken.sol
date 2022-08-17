// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20Upgradeable.sol";

/**
 * @title DamnValuableToken
 * @author Damn Vulnerable DeFi (https://damnvulnerabledefi.xyz)
 */
contract DamnValuableToken is ERC20Upgradeable {

    // Decimals are set to 18 by default in `ERC20`
    constructor() {}
    function initialize(string memory name, string memory symbol, uint256 initialSupply) public virtual initializer {
    __ERC20_init(name, symbol);
    _mint(msg.sender, initialSupply);
    }
}