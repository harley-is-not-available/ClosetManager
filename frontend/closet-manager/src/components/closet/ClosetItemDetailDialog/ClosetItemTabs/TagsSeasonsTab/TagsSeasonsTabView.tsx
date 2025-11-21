// ClosetManager/frontend/closet-manager/src/components/closet/ClosetItemDetailDialog/ClosetItemTabs/TagsSeasonsTab/TagsSeasonsTabView.tsx

import type { ClosetItem } from "../../../../../types/closet/closet-item";

interface TagsSeasonsTabViewProps {
  item: ClosetItem;
}

export const TagsSeasonsTabView = ({ item }: TagsSeasonsTabViewProps) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
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
      <div>
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
    </div>
  );
};
