import type { ClosetItem } from "../../types/closet/closet-item";
import { useState } from "react";

interface ClosetItemDetailDialogProps {
  item: ClosetItem;
  onClose: () => void;
  onEdit: () => void;
}

const ClosetItemDetailDialog: React.FC<ClosetItemDetailDialogProps> = ({
  item,
  onClose,
  onEdit,
}) => {
  // Track whether the image is valid (to handle cases where the image URL is broken)
  const [isImageValid, setIsImageValid] = useState(true);

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
          <button className="btn btn-primary" onClick={onEdit}>
            Edit
          </button>
        </div>
      </div>
    </div>
  );
};

export default ClosetItemDetailDialog;
