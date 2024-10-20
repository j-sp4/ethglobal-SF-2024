"use client";

import { useState } from "react";
import Image from "next/image";
import { motion, AnimatePresence } from "framer-motion";
import { Button } from "@/components/ui/button";
import { X } from "lucide-react";

interface ImageCard {
  id: number;
  src: string;
  price: number;
}

const Card: React.FC<ImageCard & { onClick: () => void }> = ({
  id,
  src,
  price,
  onClick,
}) => (
  <motion.div
    layoutId={`card-${id}`}
    onClick={onClick}
    className="cursor-pointer relative overflow-hidden rounded-lg shadow-lg"
    whileHover={{ scale: 1.05 }}
    whileTap={{ scale: 0.95 }}
  >
    <Image
      src={src}
      alt={`Image ${id}`}
      width={300}
      height={300}
      className="w-full h-auto"
    />
    <motion.div
      className="absolute bottom-0 left-0 right-0 bg-black bg-opacity-50 text-white p-2"
      initial={{ y: "100%" }}
      animate={{ y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <p className="text-lg font-bold">${price.toFixed(2)}</p>
    </motion.div>
  </motion.div>
);

const CardGrid: React.FC<{
  cards: ImageCard[];
  onCardClick: (id: number) => void;
}> = ({ cards, onCardClick }) => (
  <motion.div
    className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4"
    initial={{ opacity: 0 }}
    animate={{ opacity: 1 }}
    exit={{ opacity: 0 }}
  >
    {cards.map((card) => (
      <Card key={card.id} {...card} onClick={() => onCardClick(card.id)} />
    ))}
  </motion.div>
);

const Modal: React.FC<{
  selectedId: number | null;
  onClose: () => void;
  cards: ImageCard[];
}> = ({ selectedId, onClose, cards }) => (
  <AnimatePresence>
    {selectedId && (
      <motion.div
        key="modal"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
        onClick={onClose}
      >
        <motion.div
          layoutId={`card-${selectedId}`}
          className="bg-white rounded-lg shadow-lg relative max-w-md w-full"
          onClick={(e) => e.stopPropagation()}
        >
          <Button
            variant="ghost"
            size="icon"
            className="absolute top-2 right-2 z-10"
            onClick={onClose}
            aria-label="Close modal"
          >
            <X className="h-4 w-4" />
          </Button>
          <Image
            src={cards.find((card) => card.id === selectedId)?.src || ""}
            alt={`Image ${selectedId}`}
            width={400}
            height={400}
            className="w-full h-auto rounded-t-lg"
          />
          <div className="p-4">
            <h2 className="text-2xl font-bold mb-2">Image {selectedId}</h2>
            <p className="text-gray-600 mb-4">
              This is a detailed description of Image {selectedId}.
            </p>
            <motion.div
              initial={{ y: 50, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{
                delay: 0.2,
                type: "spring",
                stiffness: 300,
                damping: 25,
              }}
            >
              <Button className="w-full" size="lg">
                Buy for $5
              </Button>
            </motion.div>
          </div>
        </motion.div>
      </motion.div>
    )}
  </AnimatePresence>
);

const imageCards: ImageCard[] = [
  { id: 1, src: "/placeholder.svg?height=300&width=300", price: 19.99 },
  { id: 2, src: "/placeholder.svg?height=300&width=300", price: 24.99 },
  { id: 3, src: "/placeholder.svg?height=300&width=300", price: 29.99 },
  { id: 4, src: "/placeholder.svg?height=300&width=300", price: 34.99 },
  { id: 5, src: "/placeholder.svg?height=300&width=300", price: 39.99 },
  { id: 6, src: "/placeholder.svg?height=300&width=300", price: 44.99 },
];

export function ImageGridComponent() {
  const [selectedId, setSelectedId] = useState<number | null>(null);

  const handleCardClick = (id: number) => {
    setSelectedId(id);
  };

  const handleCloseModal = () => {
    setSelectedId(null);
  };

  return (
    <div className="container mx-auto p-4">
      <CardGrid cards={imageCards} onCardClick={handleCardClick} />
      <Modal
        selectedId={selectedId}
        onClose={handleCloseModal}
        cards={imageCards}
      />
    </div>
  );
}
