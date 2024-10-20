"use client";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { type ReactNode, useState } from "react";
import { type State, WagmiProvider } from "wagmi";
import { DynamicWagmiConnector } from "@dynamic-labs/wagmi-connector";
import { FlowWalletConnectors } from "@dynamic-labs/flow";
import { DynamicContextProvider } from "@dynamic-labs/sdk-react-core";
import { ZeroDevSmartWalletConnectors } from "@dynamic-labs/ethereum-aa";

import { getConfig } from "@/wagmi";

export function Providers(props: {
  children: ReactNode;
  initialState?: State;
}) {
  const [config] = useState(() => getConfig());
  const [queryClient] = useState(() => new QueryClient());

  return (
    <DynamicContextProvider
      theme="auto"
      settings={{
        environmentId: "d5116454-ef88-4e1b-b193-2b06f24c86b6",
        walletConnectors: [FlowWalletConnectors, ZeroDevSmartWalletConnectors],
      }}
    >
      <WagmiProvider config={config} initialState={props.initialState}>
        <QueryClientProvider client={queryClient}>
          <DynamicWagmiConnector>{props.children}</DynamicWagmiConnector>
        </QueryClientProvider>
      </WagmiProvider>
    </DynamicContextProvider>
  );
}
