import type { ClosetItem } from "../../types/closet/closet-item";
import { useState } from "react";

interface ClosetItemDetailDialogProps {
  item: ClosetItem;
  onClose: () => void;
  onSave: (updatedItem: ClosetItem) => void;
}

const ClosetItemDetailDialog: React.FC<ClosetItemDetailDialogProps> = ({
  item,
  onClose,
  onSave,
}) => {
  // Track whether the image is valid (to handle cases where the image URL is broken)
  const [isImageValid, setIsImageValid] = useState(true);

  // Track whether we're in edit mode
  const [isEditing, setIsEditing] = useState(false);

  // Track edited item data
  const [editedItem, setEditedItem] = useState<ClosetItem>(item);

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

  const handleSave = () => {
    onSave(editedItem);
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditedItem(item);
    setIsEditing(false);
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
              {editedItem.image ? (
                <img
                  src={editedItem.image}
                  alt={editedItem.brand}
                  className="w-full max-w-xs h-64 object-cover object-center rounded-lg"
                />
              ) : (
                <div className="bg-gray-200 border-2 border-dashed rounded-xl w-full max-w-xs h-64 flex items-center justify-center">
                  <span className="text-gray-500">No Image</span>
                </div>
              )}
              <div className="mt-4 w-full">
                <label className="block text-sm font-medium mb-1">
                  Image URL
                </label>
                <input
                  type="text"
                  name="image"
                  value={editedItem.image || ""}
                  onChange={handleInputChange}
                  className="input input-bordered w-full"
                  placeholder="Enter image URL"
                />
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
                      className="input input-bordered w-full"
                      placeholder="Brand name"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-1">
                      Category
                    </label>
                    <select
                      name="category"
                      value={editedItem.category}
                      onChange={handleInputChange}
                      className="select select-bordered w-full"
                    >
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
                      <option value="longSleeve">Long Sleeve</option>
                      <option value="shortSleeve">Short Sleeve</option>
                      <option value="sweatshirt">Sweatshirt</option>
                      <option value="sweater">Sweater</option>
                      <option value="hoodie">Hoodie</option>
                      <option value="tankTop">Tank Top</option>
                      <option value="blouse">Blouse</option>
                      <option value="buttonUp">Button Up</option>
                      <option value="dress">Dress</option>
                      <option value="sundress">Sun Dress</option>
                      <option value="sweaterDress">Sweater Dress</option>
                      <option value="jumpsuit">Jumpsuit</option>
                      <option value="jeans">Jeans</option>
                      <option value="chinos">Chinos</option>
                      <option value="cargo">Cargo</option>
                      <option value="shorts">Shorts</option>
                      <option value="sweatpants">Sweatpants</option>
                      <option value="skirt">Skirt</option>
                      <option value="sweaterSkirt">Sweater Skirt</option>
                      <option value="shortSkirt">Short Skirt</option>
                      <option value="longSkirt">Long Skirt</option>
                      <option value="jacket">Jacket</option>
                      <option value="blazer">Blazer</option>
                      <option value="hoodie">Hoodie</option>
                      <option value="sweatshirt">Sweatshirt</option>
                      <option value="vest">Vest</option>
                      <option value="sweater">Sweater</option>
                      <option value="sweaterVest">Sweater Vest</option>
                      <option value="shorts">Shorts</option>
                      <option value="swimwear">Swimwear</option>
                      <option value="undergarments">Undergarments</option>
                      <option value="socks">Socks</option>
                      <option value="hat">Hat</option>
                      <option value="scarf">Scarf</option>
                      <option value="gloves">Gloves</option>
                      <option value="belt">Belt</option>
                      <option value="watch">Watch</option>
                      <option value="jewelry">Jewelry</option>
                      <option value="bag">Bag</option>
                      <option value="other">Other</option>
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

                  <div>
                    <label className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        name="secondhand"
                        checked={editedItem.secondhand}
                        onChange={handleInputChange}
                        className="checkbox checkbox-primary"
                      />
                      <span className="text-sm">Secondhand</span>
                    </label>
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-1">
                      Purchase Price ($)
                    </label>
                    <input
                      type="number"
                      name="purchasePrice"
                      value={editedItem.purchasePrice}
                      onChange={handleInputChange}
                      className="input input-bordered w-full"
                      placeholder="Purchase Price"
                      step="0.01"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-1">
                      Original Price ($)
                    </label>
                    <input
                      type="number"
                      name="originalPrice"
                      value={editedItem.originalPrice}
                      onChange={handleInputChange}
                      className="input input-bordered w-full"
                      placeholder="Original Price"
                      step="0.01"
                    />
                  </div>
                </div>

                {/* Right column */}
                <div className="space-y-4">
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
                      placeholder="Purchase Location"
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
                      Condition
                    </label>
                    <select
                      name="condition"
                      value={editedItem.condition}
                      onChange={handleInputChange}
                      className="select select-bordered w-full"
                    >
                      <option value="new">New</option>
                      <option value="likeNew">Like New</option>
                      <option value="good">Good</option>
                      <option value="fair">Fair</option>
                      <option value="poor">Poor</option>
                    </select>
                  </div>

                  <div>
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

                  <div>
                    <label className="block text-sm font-medium mb-1">
                      Seasons
                    </label>
                    <div className="flex flex-wrap gap-2">
                      <label className="flex items-center space-x-1">
                        <input
                          type="checkbox"
                          checked={editedItem.seasons.includes("spring")}
                          onChange={() => handleSeasonChange("spring")}
                          className="checkbox checkbox-primary"
                        />
                        <span className="text-sm">Spring</span>
                      </label>
                      <label className="flex items-center space-x-1">
                        <input
                          type="checkbox"
                          checked={editedItem.seasons.includes("summer")}
                          onChange={() => handleSeasonChange("summer")}
                          className="checkbox checkbox-primary"
                        />
                        <span className="text-sm">Summer</span>
                      </label>
                      <label className="flex items-center space-x-1">
                        <input
                          type="checkbox"
                          checked={editedItem.seasons.includes("fall")}
                          onChange={() => handleSeasonChange("fall")}
                          className="checkbox checkbox-primary"
                        />
                        <span className="text-sm">Fall</span>
                      </label>
                      <label className="flex items-center space-x-1">
                        <input
                          type="checkbox"
                          checked={editedItem.seasons.includes("winter")}
                          onChange={() => handleSeasonChange("winter")}
                          className="checkbox checkbox-primary"
                        />
                        <span className="text-sm">Winter</span>
                      </label>
                    </div>
                  </div>

                  <div>
                    <label className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        name="hidden"
                        checked={editedItem.hidden}
                        onChange={handleInputChange}
                        className="checkbox checkbox-primary"
                      />
                      <span className="text-sm">Hidden</span>
                    </label>
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
                      rows={2}
                    />
                  </div>

                  <div>
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
                </div>
              </div>
            </div>
          </div>

          {/* Action buttons */}
          <div className="mt-6 flex flex-col sm:flex-row gap-2 justify-end">
            <button className="btn btn-outline" onClick={handleCancel}>
              Cancel
            </button>
            <button className="btn btn-primary" onClick={handleSave}>
              Save Changes
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="modal modal-open">
      <div className="modal-box max-w-5xl">
        <h3 className="text-xl font-bold">
          {item.brand} - {item.category}
        </h3>
        <div className="flex flex-col md:flex-row gap-4 mt-4">
          <div className="w-full md:w-1/3 flex items-center justify-center">
            {item.image != undefined && isImageValid ? (
              <img
                src={item.image}
                alt={item.brand}
                className="w-full max-w-xs h-64 object-cover object-center rounded-lg"
                // Handle image errors by marking the image as invalid
                onError={() => setIsImageValid(false)}
              />
            ) : (
              // Fallback UI if the image is missing or invalid
              <div className="w-full max-w-xs h-64 flex items-center justify-center bg-base-200/50 rounded-lg">
                <span className="text-lg font-medium text-base-content/70">
                  No Image
                </span>
              </div>
            )}
          </div>
          <div className="w-full md:w-2/3 overflow-y-auto max-h-96">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="card bg-base-100 p-4">
                <p className="mb-1">
                  <strong>Brand:</strong> {item.brand}
                </p>
                <p className="mb-1">
                  <strong>Category:</strong> {item.category}
                </p>
                <p className="mb-1">
                  <strong>Subcategory:</strong> {item.subcategory}
                </p>
                <p className="mb-1">
                  <strong>Color:</strong> {item.color}
                </p>
                <p className="mb-1">
                  <strong>Size:</strong> {item.size}
                </p>
                <p className="mb-1">
                  <strong>Source:</strong> {item.source}
                </p>
                <p className="mb-1">
                  <strong>Date Acquired:</strong>{" "}
                  {item.dateAcquired.toLocaleDateString()}
                </p>
                <p className="mb-1">
                  <strong>Secondhand:</strong> {item.secondhand ? "Yes" : "No"}
                </p>
                <p className="mb-1">
                  <strong>Purchase Price:</strong> $
                  {item.purchasePrice.toFixed(2)}
                </p>
                <p className="mb-1">
                  <strong>Original Price:</strong> $
                  {item.originalPrice.toFixed(2)}
                </p>
                <p className="mb-1">
                  <strong>Purchase Location:</strong> {item.purchaseLocation}
                </p>
              </div>
              <div className="card bg-base-100 p-4">
                <p className="mb-1">
                  <strong>Material:</strong> {item.material}
                </p>
                <p className="mb-1">
                  <strong>Condition:</strong> {item.condition}
                </p>
                <p className="mb-1">
                  <strong>Condition Details:</strong> {item.conditionDetails}
                </p>
                <p className="mb-1">
                  <strong>Seasons:</strong> {item.seasons.join(", ")}
                </p>
                <p className="mb-1">
                  <strong>Hidden:</strong> {item.hidden ? "Yes" : "No"}
                </p>
                <p className="mb-1">
                  <strong>Tags:</strong> {item.tags.join(", ")}
                </p>
                <p className="mb-1">
                  <strong>Personal Note:</strong> {item.personalNote}
                </p>
                <p className="mb-1">
                  <strong>Description:</strong> {item.description}
                </p>
              </div>
            </div>
          </div>
        </div>
        <div className="modal-action mt-4 flex flex-col sm:flex-row gap-2">
          <button className="btn btn-ghost" onClick={onClose}>
            Close
          </button>
          <button
            className="btn btn-primary"
            onClick={() => setIsEditing(true)}
          >
            Edit
          </button>
        </div>
      </div>
    </div>
  );
};

export default ClosetItemDetailDialog;
