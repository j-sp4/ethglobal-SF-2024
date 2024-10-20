// SPDX-License-Identifier: MIT
pragma solidity ^0.8.27;

contract Swapped {
    event VideoSwapped(
        address indexed user,
        uint256 indexed tokenId,
        string videoHash
    );

    function postSwap(uint256 _tokenId, string memory _videoHash) external {
        emit VideoSwapped(msg.sender, _tokenId, _videoHash);
    }
}
