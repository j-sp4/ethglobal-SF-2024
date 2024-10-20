import { createSchema, createModel } from '@kenthackenberry/ignition';
import { SwappedFaceNFT } from '../contracts/SwappedFaceNFT';

const schema = createSchema({
  name: 'SwappedFaceNFT',
  contractName: 'SwappedFaceNFT',
  abi: SwappedFaceNFT.abi,
  functions: {
    tokenCounter: {},
    purchasePrice: {},
    usageBaseFee: {},
    usdcToken: {},
    registerFace: {
      args: ['faceHash'],
    },
    updatePurchasePrice: {
      args: ['faceHash', 'newPurchasePrice'],
    },
    updateUsageBaseFee: {
      args: ['newUsageBaseFee'],
    },
    calculateUsageFee: {
      args: ['videoLength'],
    },
    useFace: {
      args: ['tokenId', 'videoHash', 'videoLength'],
    },
    purchaseFaceNFT: {
      args: ['faceHash'],
    },
    getFaceHash: {
      args: ['tokenId'],
    },
  },
  events: {
    FaceRegistered: {
      args: ['owner', 'faceHash'],
    },
    PurchasePriceUpdated: {
      args: ['newPurchasePrice', 'oldPurchasePrice', 'faceId'],
    },
    UsageBaseFeeUpdated: {
      args: ['newUsageBaseFee'],
    },
    FaceUsed: {
      args: ['tokenId', 'faceHash', 'videoHash', 'videoLength'],
    },
    FaceMintedFrom: {
      args: ['nftOwner', 'purchasePrice', 'tokenId', 'faceHash'],
    },
  },
});

export const SwappedFaceNFTModel = createModel(schema);
