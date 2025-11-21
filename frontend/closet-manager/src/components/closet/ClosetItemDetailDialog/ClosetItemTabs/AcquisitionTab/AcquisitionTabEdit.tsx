// ClosetManager/frontend/closet-manager/src/components/closet/ClosetItemDetailDialog/ClosetItemTabs/AcquisitionTab/AcquisitionTabEdit.tsx

import type { ClosetItem } from "../../../../../types/closet/closet-item";

interface AcquisitionTabEditProps {
  item: ClosetItem;
  onChange: (updatedItem: ClosetItem) => void;
  errors: Record<string, string>;
}

export const AcquisitionTabEdit = ({
  item,
  onChange,
  errors,
}: AcquisitionTabEditProps) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label className="block text-sm font-medium mb-1">Date Acquired</label>
        <input
          type="date"
          name="dateAcquired"
          value={
            item.dateAcquired
              ? new Date(item.dateAcquired).toISOString().split("T")[0]
              : ""
          }
          onChange={(e) =>
            onChange({ ...item, dateAcquired: new Date(e.target.value) })
          }
          className="input input-bordered w-full"
        />
      </div>
      <div>
        <label className="block text-sm font-medium mb-1">Secondhand</label>
        <input
          type="checkbox"
          name="secondhand"
          checked={item.secondhand}
          onChange={(e) => onChange({ ...item, secondhand: e.target.checked })}
          className="checkbox"
        />
        <span className="ml-2">Is this a secondhand item?</span>
      </div>
      <div>
        <label className="block text-sm font-medium mb-1">Purchase Price</label>
        <input
          type="number"
          name="purchasePrice"
          value={item.purchasePrice}
          onChange={(e) =>
            onChange({ ...item, purchasePrice: Number(e.target.value) })
          }
          className="input input-bordered w-full"
          placeholder="Purchase price"
        />
      </div>
      <div>
        <label className="block text-sm font-medium mb-1">Original Price</label>
        <input
          type="number"
          name="originalPrice"
          value={item.originalPrice}
          onChange={(e) =>
            onChange({ ...item, originalPrice: Number(e.target.value) })
          }
          className="input input-bordered w-full"
          placeholder="Original price"
        />
      </div>
      <div className="md:col-span-2">
        <label className="block text-sm font-medium mb-1">
          Purchase Location
        </label>
        <input
          type="text"
          name="purchaseLocation"
          value={item.purchaseLocation}
          onChange={(e) =>
            onChange({ ...item, purchaseLocation: e.target.value })
          }
          className="input input-bordered w-full"
          placeholder="Purchase location"
        />
      </div>
      <div className="md:col-span-2">
        <label className="block text-sm font-medium mb-1">Source</label>
        <input
          type="text"
          name="source"
          value={item.source}
          onChange={(e) => onChange({ ...item, source: e.target.value })}
          className="input input-bordered w-full"
          placeholder="Source"
        />
      </div>
    </div>
  );
};
