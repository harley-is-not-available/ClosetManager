import type { ClosetItem } from "../../types/closet/closet-item";

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
  return (
    <div className="modal modal-open">
      <div className="modal-box w-11/12 max-w-5xl">
        <h3 className="text-lg font-bold">
          {item.brand} - {item.category}
        </h3>
        <div className="flex flex-col md:flex-row gap-4 mt-4">
          <div className="w-full md:w-1/3 flex items-center justify-center">
            <img
              src={item.image}
              alt={item.brand}
              className="w-full max-w-xs h-64 object-cover object-center rounded-lg"
            />
          </div>
          <div className="w-full md:w-2/3 overflow-y-auto max-h-96">
            <div className="grid grid-cols-1 gap-4">
              <div>
                <p>
                  <strong>Brand:</strong> {item.brand}
                </p>
                <p>
                  <strong>Category:</strong> {item.category}
                </p>
                <p>
                  <strong>Subcategory:</strong> {item.subcategory}
                </p>
                <p>
                  <strong>Color:</strong> {item.color}
                </p>
                <p>
                  <strong>Size:</strong> {item.size}
                </p>
                <p>
                  <strong>Source:</strong> {item.source}
                </p>
                <p>
                  <strong>Date Acquired:</strong>{" "}
                  {item.dateAcquired.toLocaleDateString()}
                </p>
                <p>
                  <strong>Secondhand:</strong> {item.secondhand ? "Yes" : "No"}
                </p>
                <p>
                  <strong>Purchase Price:</strong> $
                  {item.purchasePrice.toFixed(2)}
                </p>
                <p>
                  <strong>Original Price:</strong> $
                  {item.originalPrice.toFixed(2)}
                </p>
                <p>
                  <strong>Purchase Location:</strong> {item.purchaseLocation}
                </p>
              </div>
              <div>
                <p>
                  <strong>Material:</strong> {item.material}
                </p>
                <p>
                  <strong>Condition:</strong> {item.condition}
                </p>
                <p>
                  <strong>Condition Details:</strong> {item.conditionDetails}
                </p>
                <p>
                  <strong>Seasons:</strong> {item.seasons.join(", ")}
                </p>
                <p>
                  <strong>Hidden:</strong> {item.hidden ? "Yes" : "No"}
                </p>
                <p>
                  <strong>Tags:</strong> {item.tags.join(", ")}
                </p>
                <p>
                  <strong>Personal Note:</strong> {item.personalNote}
                </p>
                <p>
                  <strong>Description:</strong> {item.description}
                </p>
              </div>
            </div>
          </div>
        </div>
        <div className="mt-4 flex flex-col sm:flex-row gap-2">
          <button className="btn btn-primary" onClick={onClose}>
            Close
          </button>
          <button className="btn btn-secondary" onClick={onEdit}>
            Edit
          </button>
        </div>
      </div>
    </div>
  );
};

export default ClosetItemDetailDialog;
