"use client";

import { DynamicWidget } from "@dynamic-labs/sdk-react-core";
import { Input } from "@/components/ui/input";
import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { useAccount, useWriteContract } from "wagmi";
import abi from "@/abi.json";
import { keccak256, toBytes } from "viem";

const PUBLISHER_URL =
  "http://walrus.sui.thepassivetrust.com:9001/v1/store?epochs=5";

const CONTRACT_ADDRESS = "0x055E6A527A3D4030313410035e3FaDE76Db2679C";

const Market: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [blobId, setBlobId] = useState<string | null>(null);
  const { address } = useAccount();

  const uploadMutation = useMutation({
    mutationFn: async (file: File) => {
      const formData = new FormData();
      formData.append("file", file);
      const response = await fetch(PUBLISHER_URL, {
        method: "PUT",
        body: formData,
      });
      const result = await response.json();
      console.log("Upload result:", result);
      return result;
    },
    onSuccess: (data) => {
      const newBlobId = data.newlyCreated.blobObject.blobId;
      setBlobId(newBlobId);
    },
  });

  const {
    writeContract,
    isPending: isWriteLoading,
    isSuccess: isWriteSuccess,
  } = useWriteContract();

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      console.log("File selected:", selectedFile.name);
    }
  };

  const handleUpload = () => {
    if (file) {
      uploadMutation.mutate(file);
    }
  };

  const handleRegisterFace = async () => {
    if (blobId && writeContract) {
      const faceHash = keccak256(toBytes(blobId));
      writeContract({
        address: CONTRACT_ADDRESS as `0x${string}`,
        abi,
        functionName: "registerFace",
        args: [faceHash],
      });
    }
  };

  return (
    <div className="w-full">
      <div>
        <DynamicWidget />
      </div>
      <div>
        <Input
          type="file"
          onChange={handleFileChange}
          accept=".jpg,.jpeg,.png,.gif,.mp4"
        />
        <button
          onClick={handleUpload}
          disabled={!file || uploadMutation.isPending}
        >
          Upload
        </button>
        {uploadMutation.isPending && <p>Uploading...</p>}
        {uploadMutation.isError && (
          <p>Error uploading file: {uploadMutation.error?.message}</p>
        )}
        {uploadMutation.isSuccess && (
          <>
            <p>File uploaded successfully. BlobId: {blobId}</p>
            <button
              onClick={handleRegisterFace}
              disabled={!blobId || isWriteLoading}
            >
              Register Face
            </button>
          </>
        )}
        {isWriteLoading && <p>Registering face...</p>}
        {isWriteSuccess && <p>Face registered successfully!</p>}
      </div>
    </div>
  );
};

export default Market;
