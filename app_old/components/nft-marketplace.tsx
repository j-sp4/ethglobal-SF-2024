'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter } from "@/components/ui/card"
import { LogIn, LogOut, User } from "lucide-react"

// Mock data for NFTs
const mockNFTs = [
  { id: 1, price: 0.1, image: "/placeholder.svg?height=200&width=200" },
  { id: 2, price: 0.2, image: "/placeholder.svg?height=200&width=200" },
  { id: 3, price: 0.15, image: "/placeholder.svg?height=200&width=200" },
  { id: 4, price: 0.08, image: "/placeholder.svg?height=200&width=200" },
]

export function NftMarketplace() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [balance, setBalance] = useState(1.5)
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  const handleLogin = () => {
    setIsLoggedIn(true)
    // In a real app, you'd handle authentication here
  }

  const handleLogout = () => {
    setIsLoggedIn(false)
    setIsMenuOpen(false)
    // In a real app, you'd handle logout here
  }

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen)
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Top bar */}
      <header className="bg-white shadow-md p-4 flex justify-between items-center">
        <h1 className="text-2xl font-bold">NFT Market</h1>
        <div className="relative">
          <Avatar
            className="cursor-pointer"
            onClick={toggleMenu}
          >
            <AvatarImage src="/placeholder.svg?height=40&width=40" alt="User" />
            <AvatarFallback><User /></AvatarFallback>
          </Avatar>
          <AnimatePresence>
            {isMenuOpen && (
              <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.2 }}
                className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-2 z-10"
              >
                {isLoggedIn ? (
                  <>
                    <div className="px-4 py-2">
                      <p className="text-sm font-medium text-gray-900">Welcome, User!</p>
                      <p className="text-sm text-gray-500">Balance: {balance} ETH</p>
                    </div>
                    <Button
                      onClick={handleLogout}
                      variant="ghost"
                      className="w-full justify-start px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                    >
                      <LogOut className="mr-2 h-4 w-4" /> Log out
                    </Button>
                  </>
                ) : (
                  <Button
                    onClick={handleLogin}
                    variant="ghost"
                    className="w-full justify-start px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                  >
                    <LogIn className="mr-2 h-4 w-4" /> Log in
                  </Button>
                )}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </header>

      {/* Main content */}
      <main className="p-4 md:p-8">
        <h2 className="text-3xl font-bold mb-6">Featured NFTs</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {mockNFTs.map((nft) => (
            <motion.div
              key={nft.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
            >
              <Card className="overflow-hidden h-full flex flex-col">
                <CardContent className="p-0 flex-grow">
                  <img src={nft.image} alt={`NFT ${nft.id}`} className="w-full h-48 object-cover" />
                </CardContent>
                <CardFooter className="flex justify-between items-center">
                  <span className="font-semibold">{nft.price} ETH</span>
                  <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                    <Button disabled={!isLoggedIn} size="sm">
                      {isLoggedIn ? 'Buy Now' : 'Login to Buy'}
                    </Button>
                  </motion.div>
                </CardFooter>
              </Card>
            </motion.div>
          ))}
        </div>
      </main>
    </div>
  )
}