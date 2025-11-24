// ClosetManager/frontend/closet-manager/src/components/closet/ClosetItemDetailDialog/ClosetItemTabs/TagsSeasonsTab/TagsSeasonsTabEdit.tsx

import type { ClosetItem } from "../../../../../types/closet/closet-item";

interface TagsSeasonsTabEditProps {
  item: ClosetItem;
  onChange: (updatedItem: ClosetItem) => void;
  errors: Record<string, string>;
}

export const TagsSeasonsTabEdit = ({
  item,
  onChange,
  errors,
}: TagsSeasonsTabEditProps) => {
  const handleSeasonChange = (season: string) => {
    const seasons = [...item.seasons];
    const index = seasons.indexOf(season);

    if (index > -1) {
      seasons.splice(index, 1);
    } else {
      seasons.push(season);
    }

    onChange({ ...item, seasons });
  };

  const handleTagChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const tags = e.target.value
      .split(",")
      .map((tag) => tag.trim())
      .filter((tag) => tag);
    onChange({ ...item, tags });
  };

  console.log(errors);

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label className="block text-sm font-medium mb-1">Seasons</label>
        <div className="flex flex-wrap gap-2">
          {["spring", "summer", "fall", "winter"].map((season) => (
            <button
              key={season}
              type="button"
              onClick={() => handleSeasonChange(season)}
              className={`btn btn-xs ${
                item.seasons.includes(season) ? "btn-primary" : "btn-outline"
              }`}
            >
              {season}
            </button>
          ))}
        </div>
      </div>
      <div>
        <label className="block text-sm font-medium mb-1">Tags</label>
        <input
          type="text"
          value={item.tags.join(", ")}
          onChange={handleTagChange}
          className="input input-bordered w-full"
          placeholder="Enter tags separated by commas"
        />
      </div>
    </div>
  );
};
