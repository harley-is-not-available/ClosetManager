// ClosetManager/frontend/closet-manager/src/components/closet/ClosetItemDetailDialog/ClosetItemTabs/DetailsTab/DetailsTabView.tsx

import type { ClosetItem } from "../../../../../types/closet/closet-item";

interface DetailsTabViewProps {
  item: ClosetItem;
}

export const DetailsTabView = ({ item }: DetailsTabViewProps) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div className="md:col-span-2">
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Material
        </label>
        <div className="p-2 bg-base-200 rounded">{item.material}</div>
      </div>
      <div className="md:col-span-2">
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Personal Note
        </label>
        <div className="p-2 bg-base-200 rounded min-h-[60px]">
          {item.personalNote || "None"}
        </div>
      </div>
      <div className="md:col-span-2">
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Description
        </label>
        <div className="p-2 bg-base-200 rounded min-h-[60px]">
          {item.description || "None"}
        </div>
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Condition
        </label>
        <div className="p-2 bg-base-200 rounded">{item.condition}</div>
      </div>
      <div className="md:col-span-2">
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Condition Details
        </label>
        <div className="p-2 bg-base-200 rounded min-h-[60px]">
          {item.conditionDetails || "None"}
        </div>
      </div>
    </div>
  );
};
