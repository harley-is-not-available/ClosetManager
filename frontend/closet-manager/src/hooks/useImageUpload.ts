import { useState, useCallback } from "react";
import { mockUploadImage } from "../utils/api";

export const useImageUpload = () => {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadedImageUrl, setUploadedImageUrl] = useState<string | null>(null);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [originalImage, setOriginalImage] = useState<string | null>(null);

  const handleUpload = useCallback(async (file: File) => {
    setIsUploading(true);
    setUploadError(null);
    setUploadProgress(0);

    try {
      // Simulate upload progress with realistic timing
      const progressInterval = setInterval(() => {
        setUploadProgress((prev) => {
          if (prev >= 100) {
            clearInterval(progressInterval);
            return 100;
          }
          return prev + 10;
        });
      }, 100);

      // Mock upload function
      const mockUrl = await mockUploadImage(file);

      // Clear progress interval
      clearInterval(progressInterval);
      setUploadProgress(100);

      // Store the uploaded image URL
      setUploadedImageUrl(mockUrl);

      return mockUrl;
    } catch (error) {
      setUploadError("Failed to upload image. Please try again.");
      throw error;
    } finally {
      setIsUploading(false);
    }
  }, []);

  const resetUpload = useCallback(() => {
    setIsUploading(false);
    setUploadProgress(0);
    setUploadedImageUrl(null);
    setUploadError(null);
  }, []);

  const clearUploadedImage = useCallback(() => {
    setUploadedImageUrl(null);
    setUploadError(null);
  }, []);

  const setOriginalImageIfNotSet = useCallback(
    (originalImageUrl: string | null) => {
      if (originalImageUrl && !originalImage) {
        setOriginalImage(originalImageUrl);
      }
    },
    [originalImage],
  );

  const revertToOriginalImage = useCallback(() => {
    if (originalImage) {
      setUploadedImageUrl(originalImage);
    } else {
      setUploadedImageUrl(null);
    }
    setUploadError(null);
  }, [originalImage]);

  return {
    isUploading,
    uploadProgress,
    uploadedImageUrl,
    uploadError,
    handleUpload,
    resetUpload,
    clearUploadedImage,
    setOriginalImageIfNotSet,
    revertToOriginalImage,
  };
};
