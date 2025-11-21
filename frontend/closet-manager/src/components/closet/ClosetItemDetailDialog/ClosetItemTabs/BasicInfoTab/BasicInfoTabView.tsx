// ClosetManager/frontend/closet-manager/src/components/closet/ClosetItemDetailDialog/ClosetItemTabs/BasicInfoTab/BasicInfoTabView.tsx

import type { ClosetItem } from "../../../../../types/closet/closet-item";

interface BasicInfoTabViewProps {
  item: ClosetItem;
}

export const BasicInfoTabView = ({ item }: BasicInfoTabViewProps) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Brand
        </label>
        <div className="p-2 bg-base-200 rounded">{item.brand}</div>
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Category
        </label>
        <div className="p-2 bg-base-200 rounded">{item.category}</div>
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Subcategory
        </label>
        <div className="p-2 bg-base-200 rounded">{item.subcategory}</div>
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Color
        </label>
        <div className="p-2 bg-base-200 rounded">{item.color}</div>
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Size
        </label>
        <div className="p-2 bg-base-200 rounded">{item.size}</div>
      </div>
    </div>
  );
};
