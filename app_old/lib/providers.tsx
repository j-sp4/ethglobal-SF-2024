"use client";

import { DynamicContextProvider } from "@dynamic-labs/sdk-react-core";
import { EthereumWalletConnectors } from "@dynamic-labs/ethereum";
import { WagmiProvider } from "wagmi";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { DynamicWagmiConnector } from "@dynamic-labs/wagmi-connector";
import { ZeroDevSmartWalletConnectors } from "@dynamic-labs/ethereum-aa";
import { config } from "@/lib/wagmi";

export default function Providers({ children }: { children: React.ReactNode }) {
  const queryClient = new QueryClient();

  const evmNetworks = [
    {
      blockExplorerUrls: ["https://testnet.storyscan.xyz/"],
      chainId: 1513,
      chainName: "Story Protocol",
      iconUrls: ["/images/story_icon.svg"],
      name: "Story",
      nativeCurrency: {
        decimals: 18,
        name: "IP",
        symbol: "IP",
      },
      networkId: 1513,
      rpcUrls: ["https://testnet.storyrpc.io/"],
      vanityName: "Story",
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
