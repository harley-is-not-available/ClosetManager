// ClosetManager/frontend/closet-manager/src/components/closet/ClosetItemDetailDialog/ClosetItemTabs/DetailsTab/DetailsTabEdit.tsx

import type { ClosetItem } from "../../../../../types/closet/closet-item";

interface DetailsTabEditProps {
  item: ClosetItem;
  onChange: (updatedItem: ClosetItem) => void;
  errors: Record<string, string>;
}

export const DetailsTabEdit = ({
  item,
  onChange,
  errors,
}: DetailsTabEditProps) => {
  console.log(errors);
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div className="md:col-span-2">
        <label className="block text-sm font-medium mb-1">Material</label>
        <input
          type="text"
          name="material"
          value={item.material}
          onChange={(e) => onChange({ ...item, material: e.target.value })}
          className="input input-bordered w-full"
          placeholder="Material"
        />
      </div>
      <div className="md:col-span-2">
        <label className="block text-sm font-medium mb-1">Personal Note</label>
        <textarea
          name="personalNote"
          value={item.personalNote}
          onChange={(e) => onChange({ ...item, personalNote: e.target.value })}
          className="textarea textarea-bordered w-full"
          placeholder="Personal note"
          rows={3}
        />
      </div>
      <div className="md:col-span-2">
        <label className="block text-sm font-medium mb-1">Description</label>
        <textarea
          name="description"
          value={item.description}
          onChange={(e) => onChange({ ...item, description: e.target.value })}
          className="textarea textarea-bordered w-full"
          placeholder="Description"
          rows={3}
        />
      </div>
      <div>
        <label className="block text-sm font-medium mb-1">Condition</label>
        <select
          name="condition"
          value={item.condition}
          onChange={(e) => onChange({ ...item, condition: e.target.value })}
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
      <div className="md:col-span-2">
        <label className="block text-sm font-medium mb-1">
          Condition Details
        </label>
        <textarea
          name="conditionDetails"
          value={item.conditionDetails}
          onChange={(e) =>
            onChange({ ...item, conditionDetails: e.target.value })
          }
          className="textarea textarea-bordered w-full"
          placeholder="Condition details"
          rows={2}
        />
      </div>
    </div>
  );
};
