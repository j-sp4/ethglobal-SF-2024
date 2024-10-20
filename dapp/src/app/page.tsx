"use client";

import { BackgroundLines } from "@/components/ui/background-lines";
import { Button } from "@/components/ui/button";
import { DynamicWidget } from "@dynamic-labs/sdk-react-core";
import { useRouter } from "next/navigation";
import { useIsLoggedIn } from "@dynamic-labs/sdk-react-core";
import { useEffect } from "react";

function App() {
  const router = useRouter();
  const isLoggedIn = useIsLoggedIn();

  useEffect(() => {
    console.log("isLoggedIn", isLoggedIn);
    if (isLoggedIn) {
      router.push("/market");
    }
  }, [isLoggedIn]);

  return (
    <BackgroundLines className="flex items-center justify-center w-full flex-col px-4">
      <h2 className="bg-clip-text text-transparent text-center bg-gradient-to-b from-neutral-900 to-neutral-700 dark:from-neutral-600 dark:to-white text-2xl md:text-4xl lg:text-7xl font-sans py-2 md:py-10 relative z-20 font-bold tracking-tight">
        Swapped A.I.
        <br />
      </h2>
      <p className="max-w-xl mx-auto text-sm md:text-lg text-neutral-700 dark:text-neutral-400 text-center">
        An ethical deepfake AI marketplace powered by Flow.
      </p>
      <br />
      <DynamicWidget />
      {/* <Button onClick={handleGetStarted}>Get Started</Button> */}
    </BackgroundLines>
  );
}

export default App;
