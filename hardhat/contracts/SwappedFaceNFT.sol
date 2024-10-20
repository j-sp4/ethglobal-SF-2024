// SPDX-License-Identifier: MIT
pragma solidity ^0.8.27;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Burnable.sol";

contract FaceNFT is ERC721, Ownable, ERC721Burnable {
    uint256 public tokenCounter;
    uint256 public purchasePrice;
    uint256 public usageBaseFee; // Base fee to use a FaceNFT, per second of video

    IERC20 public usdcToken;

    // FaceData to Wallet Address (owner of the face)
    mapping(uint256 => address) private faceHashes;
    mapping(uint256 => uint256) private tokenIdsToFaceHashes;

    event FaceRegistered(address indexed owner, uint256 faceHash);
    event PurchasePriceUpdated(
        uint256 newPurchasePrice,
        uint256 oldPurchasePrice,
        uint256 faceId
    );
    event UsageBaseFeeUpdated(uint256 newUsageBaseFee);
    event FaceUsed(
        uint256 tokenId,
        uint256 faceHash,
        uint256 videoHash,
        uint256 videoLength
    );

    event FaceMintedFrom(
        address nftOwner,
        uint256 purchasePrice,
        uint256 tokenId,
        uint256 faceHash
    );

    constructor(
        address _usdcTokenAddress
    ) ERC721("FaceNFT", "FNT") Ownable(msg.sender) {
        tokenCounter = 1;
        purchasePrice = 5 * 10 ** 6; // 5 USDC
        usageBaseFee = 1 * 10 ** 6; // 1 USDC per second of video
        usdcToken = IERC20(_usdcTokenAddress);
    }

    function registerFace(uint256 _faceHash) external {
        require(faceHashes[_faceHash] == address(0), "Face already registered");

        faceHashes[_faceHash] = msg.sender;
        emit FaceRegistered(msg.sender, _faceHash);
    }

    function updatePurchasePrice(
        uint256 _faceHash,
        uint256 _newPurchasePrice
    ) external {
        require(
            faceHashes[_faceHash] == msg.sender,
            "Not the owner of this face"
        );

        uint256 oldPurchasePrice = purchasePrice;

        purchasePrice = _newPurchasePrice;
        emit PurchasePriceUpdated(
            _newPurchasePrice,
            oldPurchasePrice,
            _faceHash
        );
    }

    function updateUsageBaseFee(uint256 _newUsageBaseFee) external onlyOwner {
        usageBaseFee = _newUsageBaseFee;
        emit UsageBaseFeeUpdated(_newUsageBaseFee);
    }

    function calculateUsageFee(
        uint256 _videoLength
    ) public view returns (uint256) {
        return usageBaseFee * _videoLength;
    }

    function useFace(
        uint256 _tokenId,
        uint256 _videoHash,
        uint256 _videoLength
    ) external {
        require(ownerOf(_tokenId) == msg.sender, "Not the owner");

        uint256 usageFee = calculateUsageFee(_videoLength);
        require(
            usdcToken.balanceOf(msg.sender) >= usageFee,
            "Insufficient USDC balance for usage"
        );
        require(
            usdcToken.allowance(msg.sender, address(this)) >= usageFee,
            "Allowance not set for USDC usage transfer"
        );

        uint256 faceHash = tokenIdsToFaceHashes[_tokenId];

        usdcToken.transferFrom(msg.sender, owner(), usageFee);

        emit FaceUsed(_tokenId, faceHash, _videoHash, _videoLength);

        _burn(_tokenId);
        delete tokenIdsToFaceHashes[_tokenId];
    }

    function purchaseFaceNFT(uint256 _faceHash) external {
        require(faceHashes[_faceHash] != address(0), "No face registered");
        require(
            usdcToken.balanceOf(msg.sender) >= purchasePrice,
            "Insufficient USDC balance for purchase"
        );
        require(
            usdcToken.allowance(msg.sender, address(this)) >= purchasePrice,
            "Allowance not set for USDC purchase transfer"
        );
        require(faceHashes[_faceHash] != msg.sender, "Already owned");

        usdcToken.transferFrom(msg.sender, owner(), purchasePrice);

        tokenCounter += 1;
        _safeMint(msg.sender, tokenCounter);
        tokenIdsToFaceHashes[tokenCounter] = _faceHash;

        emit FaceMintedFrom(msg.sender, purchasePrice, tokenCounter, _faceHash);
    }

    function getFaceHash(uint256 _tokenId) external view returns (uint256) {
        return tokenIdsToFaceHashes[_tokenId];
    }
}
