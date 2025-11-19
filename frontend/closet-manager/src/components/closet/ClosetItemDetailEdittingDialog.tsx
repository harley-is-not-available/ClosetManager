import React, { useState } from "react";
import type { ClosetItem } from "../../types/closet/closet-item";
import { ItemCategory } from "../../types/enums/item_category";
import { ItemSubcategory } from "../../types/enums/item_subcategory";
import { ItemCondition } from "../../types/enums/item_condition";
import { ItemSeason, type ItemSeasonKey } from "../../types/enums/item_season";

interface ClosetItemDetailEdittingDialogProps {
  item: ClosetItem;
  onClose: () => void;
  onSave: (updatedItem: ClosetItem) => void;
}

const ClosetItemDetailEdittingDialog: React.FC<
  ClosetItemDetailEdittingDialogProps
> = ({ item, onClose, onSave }) => {
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

  const handleSeasonChange = (season: ItemSeasonKey) => {
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
  };

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
                    {Object.entries(ItemCategory).map(([key, value]) => (
                      <option key={key} value={value}>
                        {value}
                      </option>
                    ))}
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
                    {Object.entries(ItemSubcategory).map(([key, value]) => (
                      <option key={key} value={value}>
                        {value}
                      </option>
                    ))}
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
                  <label className="block text-sm font-medium mb-1">Size</label>
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
                    value={editedItem.dateAcquired.toISOString().split("T")[0]}
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
                    {Object.entries(ItemCondition).map(([key, value]) => (
                      <option key={key} value={value}>
                        {value}
                      </option>
                    ))}
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
                    {Object.entries(ItemSeason).map(([key, value]) => (
                      <label key={key} className="flex items-center space-x-1">
                        <input
                          type="checkbox"
                          checked={editedItem.seasons.includes(value)}
                          onChange={() => handleSeasonChange(value)}
                          className="checkbox checkbox-primary"
                        />
                        <span className="text-sm">{value}</span>
                      </label>
                    ))}
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
                  <label className="block text-sm font-medium mb-1">Tags</label>
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
          <button className="btn btn-outline" onClick={onClose}>
            Cancel
          </button>
          <button className="btn btn-primary" onClick={handleSave}>
            Save Changes
          </button>
        </div>
      </div>
    </div>
  );
};

export default ClosetItemDetailEdittingDialog;
