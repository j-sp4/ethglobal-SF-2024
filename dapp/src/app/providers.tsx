"use client";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { type ReactNode, useState } from "react";
import { type State, WagmiProvider } from "wagmi";
import { DynamicWagmiConnector } from "@dynamic-labs/wagmi-connector";
import { DynamicContextProvider } from "@dynamic-labs/sdk-react-core";
import { EthereumWalletConnectors } from "@dynamic-labs/ethereum";
import { ZeroDevSmartWalletConnectors } from "@dynamic-labs/ethereum-aa";

import { getConfig } from "@/wagmi";

export function Providers({
  children,
  initialState,
}: {
  children: ReactNode;
  initialState?: State;
}) {
  const [config] = useState(() => getConfig());
  const [queryClient] = useState(() => new QueryClient());

  const evmNetworks = [
    {
      blockExplorerUrls: ["https://evm-testnet.flowscan.io"],
      chainId: 545,
      chainName: "EVM on Flow Testnet",
      iconUrls: [
        "https://cdn.prod.website-files.com/5f734f4dbd95382f4fdfa0ea/6395e6749db8fe00a41cc279_flow-flow-logo.svg",
      ],
      name: "Flow",
      nativeCurrency: {
        decimals: 18,
        name: "FLOW",
        symbol: "FLOW",
      },
      networkId: 545,
      rpcUrls: ["https://testnet.evm.nodes.onflow.org"],
      vanityName: "Flow",
    },
  ];

  return (
    <DynamicContextProvider
      theme="auto"
      settings={{
        environmentId: "d5116454-ef88-4e1b-b193-2b06f24c86b6",
        walletConnectors: [
          EthereumWalletConnectors,
          ZeroDevSmartWalletConnectors,
        ],
        overrides: {
          evmNetworks,
        },
      }}
    >
      <WagmiProvider config={config}>
        <QueryClientProvider client={queryClient}>
          <DynamicWagmiConnector>{children}</DynamicWagmiConnector>
        </QueryClientProvider>
      </WagmiProvider>
    </DynamicContextProvider>
  );
}
