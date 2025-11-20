import type { ClosetItem } from "../../types/closet/closet-item";
import { useState, useEffect } from "react";
import { useImageUpload } from "../../hooks/useImageUpload";

interface ClosetItemDetailDialogProps {
  item: ClosetItem;
  onClose: () => void;
  onSave: (updatedItem: ClosetItem) => void;
  isEditing?: boolean;
}

const ClosetItemDetailDialog: React.FC<ClosetItemDetailDialogProps> = ({
  item,
  onClose,
  onSave,
  isEditing: initialIsEditing = false,
}) => {
  // Track whether we're in edit mode
  const [isEditing, setIsEditing] = useState(initialIsEditing);

  // Track edited item data
  const [editedItem, setEditedItem] = useState<ClosetItem>(item);

  // Track validation errors
  const [errors, setErrors] = useState<Record<string, string>>({});

  // Track whether the image is valid (to handle cases where the image URL is broken)
  const [isImageValid, setIsImageValid] = useState(true);

  // Use the image upload hook
  const {
    isUploading,
    uploadProgress,
    uploadedImageUrl,
    uploadError,
    handleUpload,
    resetUpload,
    clearUploadedImage,
    setOriginalImageIfNotSet,
    revertToOriginalImage,
  } = useImageUpload();

  // Set original image when component loads
  useEffect(() => {
    setOriginalImageIfNotSet(item.image || null);
  }, [item.image, setOriginalImageIfNotSet]);

  // Update edited item when image is uploaded
  useEffect(() => {
    if (uploadedImageUrl !== null && uploadedImageUrl !== undefined) {
      setEditedItem((prev) => ({
        ...prev,
        image: uploadedImageUrl,
      }));
    }
  }, [uploadedImageUrl]);

  // Track if we have an uploaded image that can be reverted (not just the original)
  const hasUploadedImage =
    uploadedImageUrl !== null &&
    uploadedImageUrl !== undefined &&
    item.image !== uploadedImageUrl;

  // Reset upload state when component unmounts
  useEffect(() => {
    return () => {
      resetUpload();
    };
  }, [resetUpload]);

  const handleInputChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement
    >,
  ) => {
    const { name, value } = e.target;

    // Handle different input types
    if (e.target.type === "checkbox") {
      const checkbox = e.target as HTMLInputElement;
      setEditedItem({
        ...editedItem,
        [name]: checkbox.checked,
      });
    } else if (name === "dateAcquired") {
      setEditedItem({
        ...editedItem,
        [name]: new Date(value),
      });
    } else {
      setEditedItem({
        ...editedItem,
        [name]: value,
      });
    }

    // Clear error when user starts typing
    if (errors[name]) {
      setErrors({
        ...errors,
        [name]: "",
      });
    }
  };

  const handleSeasonChange = (season: string) => {
    const seasons = [...editedItem.seasons];
    const index = seasons.indexOf(season);

    if (index > -1) {
      seasons.splice(index, 1);
    } else {
      seasons.push(season);
    }

    setEditedItem({
      ...editedItem,
      seasons,
    });
  };

  const handleTagChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const tags = e.target.value
      .split(",")
      .map((tag) => tag.trim())
      .filter((tag) => tag);
    setEditedItem({
      ...editedItem,
      tags,
    });
  };

  const validateFields = () => {
    const newErrors: Record<string, string> = {};

    if (!editedItem.brand.trim()) {
      newErrors.brand = "Brand is required";
    }

    if (!editedItem.category.trim()) {
      newErrors.category = "Category is required";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSave = () => {
    if (validateFields()) {
      // Before saving, handle image logic properly
      let itemToSave = { ...editedItem };

      // If an image was uploaded, use the uploaded image URL
      if (uploadedImageUrl !== null && uploadedImageUrl !== undefined) {
        itemToSave.image = uploadedImageUrl;
      }
      // If no image was uploaded but there was an existing image, keep it
      // If no image was uploaded and there was no existing image, leave as undefined

      onSave(itemToSave);
      setIsEditing(false);

      // Reset upload state after saving
      resetUpload();
    }
  };

  const handleCancel = () => {
    // Reset upload state when canceling
    resetUpload();
    setEditedItem(item);
    setIsEditing(false);
    setErrors({});
    onClose();
  };

  const validateFile = (file: File): string | null => {
    // Validate file type
    if (!file.type.startsWith("image/")) {
      return "Please select an image file (JPEG, PNG, etc.)";
    }

    // Validate file size (limit to 5MB)
    if (file.size > 5 * 1024 * 1024) {
      return "File size exceeds 5MB limit";
    }

    return null;
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      const error = validateFile(file);

      if (error) {
        // We don't need to setUploadError here as it's handled by the hook's callback
        return;
      }

      // Reset any previous upload errors
      // In the current implementation we let the hook handle error state

      // Upload the file
      handleUpload(file);
    }
  };

  if (isEditing) {
    return (
      <div className="modal modal-open">
        <div className="modal-box w-11/12 max-w-5xl">
          <h3 className="text-lg font-bold">
            Edit {editedItem.brand} - {editedItem.category}
          </h3>

          <div className="flex flex-col md:flex-row gap-4 mt-4">
            {/* Image section */}
            <div className="w-full md:w-1/3 flex flex-col items-center justify-center">
              {/* Image display logic */}
              {editedItem.image || uploadedImageUrl ? (
                <div className="relative">
                  <img
                    src={editedItem.image || uploadedImageUrl!}
                    alt={editedItem.brand}
                    className="w-full max-w-xs h-64 object-cover object-center rounded-lg"
                    onError={() => setIsImageValid(false)}
                  />
                  {editedItem.image && (
                    <div className="absolute top-2 right-2 flex gap-1">
                      {hasUploadedImage && (
                        <button
                          onClick={revertToOriginalImage}
                          className="bg-blue-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs"
                          aria-label="Revert to original image"
                        >
                          ↺
                        </button>
                      )}
                    </div>
                  )}
                </div>
              ) : (
                <div className="bg-gray-200 border-2 border-dashed rounded-xl w-full max-w-xs h-64 flex items-center justify-center">
                  <span className="text-gray-500">No Image</span>
                </div>
              )}

              {/* Upload button and file input */}
              <div className="mt-4 w-full">
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleFileChange}
                  className="hidden"
                  id="image-upload-input"
                />
                <label
                  htmlFor="image-upload-input"
                  className="btn btn-secondary w-full"
                  aria-describedby="image-upload-description"
                >
                  {isUploading ? "Uploading..." : "Select Image"}
                </label>

                {/* Accessibility description */}
                <span id="image-upload-description" className="sr-only">
                  Choose an image file to upload. Supported formats: JPEG, PNG,
                  etc.
                </span>

                {uploadError && (
                  <p className="text-red-500 text-sm mt-2">{uploadError}</p>
                )}

                {isUploading && (
                  <div className="mt-2">
                    <div className="w-full bg-gray-200 rounded-full h-2.5">
                      <div
                        className="bg-blue-600 h-2.5 rounded-full"
                        style={{ width: `${uploadProgress}%` }}
                      ></div>
                    </div>
                    <p className="text-sm text-gray-600 mt-1">
                      {uploadProgress}%
                    </p>
                  </div>
                )}
              </div>
            </div>

            {/* Editable fields section */}
            <div className="w-full md:w-2/3 overflow-y-auto max-h-96">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Left column */}
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium mb-1">
                      Brand
                    </label>
                    <input
                      type="text"
                      name="brand"
                      value={editedItem.brand}
                      onChange={handleInputChange}
                      className={`input input-bordered w-full ${errors.brand ? "input-error" : ""}`}
                      placeholder="Brand name"
                    />
                    {errors.brand && (
                      <span className="text-error text-sm mt-1">
                        {errors.brand}
                      </span>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-1">
                      Category
                    </label>
                    <select
                      name="category"
                      value={editedItem.category}
                      onChange={handleInputChange}
                      className={`select select-bordered w-full ${errors.category ? "select-error" : ""}`}
                    >
                      <option value="">Select category</option>
                      <option value="tShirt">T-Shirt</option>
                      <option value="jeans">Jeans</option>
                      <option value="dress">Dress</option>
                      <option value="jacket">Jacket</option>
                      <option value="sweater">Sweater</option>
                      <option value="skirt">Skirt</option>
                      <option value="pants">Pants</option>
                      <option value="shoes">Shoes</option>
                      <option value="accessory">Accessory</option>
                      <option value="other">Other</option>
                    </select>
                    {errors.category && (
                      <span className="text-error text-sm mt-1">
                        {errors.category}
                      </span>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-1">
                      Subcategory
                    </label>
                    <select
                      name="subcategory"
                      value={editedItem.subcategory}
                      onChange={handleInputChange}
                      className="select select-bordered w-full"
                    >
                      <option value="">Select subcategory</option>
                      <option value="tShirt">T-Shirt</option>
                      <option value="sweater">Sweater</option>
                      <option value="hoodie">Hoodie</option>
                      <option value="jeans">Jeans</option>
                      <option value="dress">Dress</option>
                      <option value="skirt">Skirt</option>
                      <option value="sweatpants">Sweatpants</option>
                      <option value="jacket">Jacket</option>
                      <option value="sneakers">Sneakers</option>
                      <option value="baseballCap">Baseball Cap</option>
                      <option value="winterCoat">Winter Coat</option>
                      <option value="maxiSkirt">Maxi Skirt</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-1">
                      Color
                    </label>
                    <input
                      type="text"
                      name="color"
                      value={editedItem.color}
                      onChange={handleInputChange}
                      className="input input-bordered w-full"
                      placeholder="Color"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-1">
                      Size
                    </label>
                    <input
                      type="text"
                      name="size"
                      value={editedItem.size}
                      onChange={handleInputChange}
                      className="input input-bordered w-full"
                      placeholder="Size"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-1">
                      Source
                    </label>
                    <input
                      type="text"
                      name="source"
                      value={editedItem.source}
                      onChange={handleInputChange}
                      className="input input-bordered w-full"
                      placeholder="Source"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-1">
                      Date Acquired
                    </label>
                    <input
                      type="date"
                      name="dateAcquired"
                      value={
                        editedItem.dateAcquired.toISOString().split("T")[0]
                      }
                      onChange={handleInputChange}
                      className="input input-bordered w-full"
                    />
                  </div>
                </div>

                {/* Right column */}
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium mb-1">
                      Secondhand
                    </label>
                    <input
                      type="checkbox"
                      name="secondhand"
                      checked={editedItem.secondhand}
                      onChange={handleInputChange}
                      className="checkbox"
                    />
                    <span className="ml-2">Is this a secondhand item?</span>
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-1">
                      Purchase Price
                    </label>
                    <input
                      type="number"
                      name="purchasePrice"
                      value={editedItem.purchasePrice}
                      onChange={handleInputChange}
                      className="input input-bordered w-full"
                      placeholder="Purchase price"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-1">
                      Original Price
                    </label>
                    <input
                      type="number"
                      name="originalPrice"
                      value={editedItem.originalPrice}
                      onChange={handleInputChange}
                      className="input input-bordered w-full"
                      placeholder="Original price"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-1">
                      Purchase Location
                    </label>
                    <input
                      type="text"
                      name="purchaseLocation"
                      value={editedItem.purchaseLocation}
                      onChange={handleInputChange}
                      className="input input-bordered w-full"
                      placeholder="Purchase location"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-1">
                      Material
                    </label>
                    <input
                      type="text"
                      name="material"
                      value={editedItem.material}
                      onChange={handleInputChange}
                      className="input input-bordered w-full"
                      placeholder="Material"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-1">
                      Personal Note
                    </label>
                    <textarea
                      name="personalNote"
                      value={editedItem.personalNote}
                      onChange={handleInputChange}
                      className="textarea textarea-bordered w-full"
                      placeholder="Personal note"
                      rows={3}
                    />
                  </div>
                </div>
              </div>

              {/* Seasons and tags */}
              <div className="mt-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-1">
                      Seasons
                    </label>
                    <div className="flex flex-wrap gap-2">
                      {["spring", "summer", "fall", "winter"].map((season) => (
                        <button
                          key={season}
                          type="button"
                          onClick={() => handleSeasonChange(season)}
                          className={`btn btn-xs ${
                            editedItem.seasons.includes(season)
                              ? "btn-primary"
                              : "btn-outline"
                          }`}
                        >
                          {season}
                        </button>
                      ))}
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-1">
                      Tags
                    </label>
                    <input
                      type="text"
                      value={editedItem.tags.join(", ")}
                      onChange={handleTagChange}
                      className="input input-bordered w-full"
                      placeholder="Enter tags separated by commas"
                    />
                  </div>
                </div>
              </div>

              {/* Description */}
              <div className="mt-6">
                <label className="block text-sm font-medium mb-1">
                  Description
                </label>
                <textarea
                  name="description"
                  value={editedItem.description}
                  onChange={handleInputChange}
                  className="textarea textarea-bordered w-full"
                  placeholder="Description"
                  rows={3}
                />
              </div>

              {/* Condition */}
              <div className="mt-6">
                <label className="block text-sm font-medium mb-1">
                  Condition
                </label>
                <select
                  name="condition"
                  value={editedItem.condition}
                  onChange={handleInputChange}
                  className="select select-bordered w-full"
                >
                  <option value="">Select condition</option>
                  <option value="new">New</option>
                  <option value="likeNew">Like New</option>
                  <option value="good">Good</option>
                  <option value="fair">Fair</option>
                  <option value="poor">Poor</option>
                </select>
              </div>

              {/* Condition Details */}
              <div className="mt-4">
                <label className="block text-sm font-medium mb-1">
                  Condition Details
                </label>
                <textarea
                  name="conditionDetails"
                  value={editedItem.conditionDetails}
                  onChange={handleInputChange}
                  className="textarea textarea-bordered w-full"
                  placeholder="Condition details"
                  rows={2}
                />
              </div>

              {/* Hidden */}
              <div className="mt-6">
                <label className="block text-sm font-medium mb-1">Hidden</label>
                <input
                  type="checkbox"
                  name="hidden"
                  checked={editedItem.hidden}
                  onChange={handleInputChange}
                  className="checkbox"
                />
                <span className="ml-2">Hide this item from view</span>
              </div>

              {/* Action buttons */}
              <div className="mt-8 flex justify-end gap-3">
                <button className="btn btn-ghost" onClick={handleCancel}>
                  Cancel
                </button>
                <button className="btn btn-primary" onClick={handleSave}>
                  Save Changes
                </button>
              </div>
            </div>
          </div>
        </div>
        <div className="modal-backdrop" onClick={onClose}></div>
      </div>
    );
  }

  // View mode - show item details without edit controls
  if (!isEditing) {
    return (
      <div className="modal modal-open">
        <div className="modal-box max-w-4xl w-full max-h-[90vh] overflow-y-auto">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-xl font-bold">{item.brand}</h3>
            <button
              className="btn btn-sm btn-circle btn-ghost"
              onClick={onClose}
            >
              ✕
            </button>
          </div>

          <div className="flex flex-col md:flex-row gap-6">
            {/* Image section */}
            <div className="w-full md:w-1/3 flex flex-col items-center">
              {item.image ? (
                <img
                  src={item.image}
                  alt={item.brand}
                  className="w-full max-w-xs h-64 object-cover object-center rounded-lg"
                />
              ) : (
                <div className="bg-gray-200 border-2 border-dashed rounded-xl w-full max-w-xs h-64 flex items-center justify-center">
                  <span className="text-gray-500">No Image</span>
                </div>
              )}
            </div>

            {/* Details section */}
            <div className="w-full md:w-2/3">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Brand */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Brand
                  </label>
                  <div className="p-2 bg-base-200 rounded">{item.brand}</div>
                </div>

                {/* Category */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Category
                  </label>
                  <div className="p-2 bg-base-200 rounded">{item.category}</div>
                </div>

                {/* Subcategory */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Subcategory
                  </label>
                  <div className="p-2 bg-base-200 rounded">
                    {item.subcategory}
                  </div>
                </div>

                {/* Color */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Color
                  </label>
                  <div className="p-2 bg-base-200 rounded">{item.color}</div>
                </div>

                {/* Size */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Size
                  </label>
                  <div className="p-2 bg-base-200 rounded">{item.size}</div>
                </div>

                {/* Source */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Source
                  </label>
                  <div className="p-2 bg-base-200 rounded">{item.source}</div>
                </div>

                {/* Date Acquired */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Date Acquired
                  </label>
                  <div className="p-2 bg-base-200 rounded">
                    {item.dateAcquired
                      ? new Date(item.dateAcquired).toLocaleDateString()
                      : "Not set"}
                  </div>
                </div>

                {/* Secondhand */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Secondhand
                  </label>
                  <div className="p-2 bg-base-200 rounded">
                    {item.secondhand ? "Yes" : "No"}
                  </div>
                </div>

                {/* Purchase Price */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Purchase Price
                  </label>
                  <div className="p-2 bg-base-200 rounded">
                    ${item.purchasePrice.toFixed(2)}
                  </div>
                </div>

                {/* Original Price */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Original Price
                  </label>
                  <div className="p-2 bg-base-200 rounded">
                    ${item.originalPrice.toFixed(2)}
                  </div>
                </div>

                {/* Purchase Location */}
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Purchase Location
                  </label>
                  <div className="p-2 bg-base-200 rounded">
                    {item.purchaseLocation}
                  </div>
                </div>

                {/* Material */}
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Material
                  </label>
                  <div className="p-2 bg-base-200 rounded">{item.material}</div>
                </div>

                {/* Personal Note */}
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Personal Note
                  </label>
                  <div className="p-2 bg-base-200 rounded min-h-[60px]">
                    {item.personalNote || "None"}
                  </div>
                </div>

                {/* Description */}
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Description
                  </label>
                  <div className="p-2 bg-base-200 rounded min-h-[60px]">
                    {item.description || "None"}
                  </div>
                </div>

                {/* Condition */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Condition
                  </label>
                  <div className="p-2 bg-base-200 rounded">
                    {item.condition}
                  </div>
                </div>

                {/* Condition Details */}
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Condition Details
                  </label>
                  <div className="p-2 bg-base-200 rounded min-h-[60px]">
                    {item.conditionDetails || "None"}
                  </div>
                </div>

                {/* Seasons */}
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Seasons
                  </label>
                  <div className="flex flex-wrap gap-2">
                    {item.seasons.map((season, index) => (
                      <span key={index} className="badge badge-primary">
                        {season}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Tags */}
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Tags
                  </label>
                  <div className="flex flex-wrap gap-2">
                    {item.tags.map((tag, index) => (
                      <span key={index} className="badge badge-secondary">
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Hidden */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Hidden
                  </label>
                  <div className="p-2 bg-base-200 rounded">
                    {item.hidden ? "Yes" : "No"}
                  </div>
                </div>
              </div>

              {/* Action buttons */}
              <div className="mt-6 flex justify-end gap-3">
                <button
                  className="btn btn-primary"
                  onClick={() => setIsEditing(true)}
                >
                  Edit Item
                </button>
              </div>
            </div>
          </div>
        </div>
        <div className="modal-backdrop" onClick={onClose}></div>
      </div>
    );
  }

  return null;
};

export default ClosetItemDetailDialog;
