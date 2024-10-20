"use client";

import { AppSidebar } from "@/components/app-sidebar";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { DynamicWidget } from "@/lib/dynamic";
import { useState, useEffect } from "react";

const checkIsDarkSchemePreferred = () => {
  if (typeof window !== "undefined") {
    return window.matchMedia?.("(prefers-color-scheme:dark)")?.matches ?? false;
  }
  return false;
};

export default function Main() {
  const [isDarkMode, setIsDarkMode] = useState(checkIsDarkSchemePreferred);

  useEffect(() => {
    const darkModeMediaQuery = window.matchMedia(
      "(prefers-color-scheme: dark)",
    );
    const handleChange = () => setIsDarkMode(checkIsDarkSchemePreferred());

    darkModeMediaQuery.addEventListener("change", handleChange);
    return () => darkModeMediaQuery.removeEventListener("change", handleChange);
  }, []);

  return (
    <div className={`container ${isDarkMode ? "dark" : "light"}`}>
      <div className="modal">
        <DynamicWidget />
        <main>
          <SidebarTrigger />
          <div> working </div>
        </main>
      </div>
    </div>
  );
}
