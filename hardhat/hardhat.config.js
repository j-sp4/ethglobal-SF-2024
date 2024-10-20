import "@nomicfoundation/hardhat-toolbox"

/** @type import('hardhat/config').HardhatUserConfig */

import "@nomiclabs/hardhat-waffle"

module.exports = {
  solidity: "0.8.27",
  paths: {
    sources: "./contracts",
    tests: "./test",
    cache: "./cache",
    artifacts: "./artifacts"
  },
  networks: {
    hardhat: {
      chainId: 1337,
    },
  },
};
