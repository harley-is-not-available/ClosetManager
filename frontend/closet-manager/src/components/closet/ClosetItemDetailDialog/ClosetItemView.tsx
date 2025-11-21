import type { ClosetItem } from "../../../types/closet/closet-item";
import { BasicInfoTabView } from "./ClosetItemTabs/BasicInfoTab/BasicInfoTabView";
import { AcquisitionTabView } from "./ClosetItemTabs/AcquisitionTab/AcquisitionTabView";
import { TagsSeasonsTabView } from "./ClosetItemTabs/TagsSeasonsTab/TagsSeasonsTabView";
import { DetailsTabView } from "./ClosetItemTabs/DetailsTab/DetailsTabView";

interface ClosetItemViewProps {
  item: ClosetItem;
  activeTab: string;
  onTabChange: (tabName: string) => void;
  onEdit: () => void;
  onClose: () => void;
}

export const ClosetItemView: React.FC<ClosetItemViewProps> = ({
  item,
  activeTab,
  onTabChange,
  onEdit,
  onClose,
}) => {
  return (
    <div className="modal modal-open">
      <div className="modal-box max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-xl font-bold">{item.brand}</h3>
          <button className="btn btn-sm btn-circle btn-ghost" onClick={onClose}>
            ✕
          </button>
        </div>

        <div className="flex flex-col md:flex-row gap-6">
          {/* Image section */}
          <div className="w-full md:w-1/3 flex flex-col items-center">
            {item.image ? (
              <img
                src={item.image}
                alt={item.brand}
                className="w-full max-w-xs h-64 object-cover object-center rounded-lg"
              />
            ) : (
              <div className="bg-gray-200 border-2 border-dashed rounded-xl w-full max-w-xs h-64 flex items-center justify-center">
                <span className="text-gray-500">No Image</span>
              </div>
            )}
          </div>

          {/* Details section - tabs */}
          <div className="w-full md:w-2/3">
            <div className="tabs tabs-bordered">
              <button
                className={`tab ${activeTab === "basicInfo" ? "tab-active" : ""}`}
                onClick={() => onTabChange("basicInfo")}
              >
                Basic Info
              </button>
              <button
                className={`tab ${activeTab === "acquisition" ? "tab-active" : ""}`}
                onClick={() => onTabChange("acquisition")}
              >
                Acquisition
              </button>
              <button
                className={`tab ${activeTab === "details" ? "tab-active" : ""}`}
                onClick={() => onTabChange("details")}
              >
                Details
              </button>
              <button
                className={`tab ${activeTab === "tagsSeasons" ? "tab-active" : ""}`}
                onClick={() => onTabChange("tagsSeasons")}
              >
                Tags & Seasons
              </button>
            </div>

            <div className="mt-4 min-h-[200px]">
              {activeTab === "basicInfo" && <BasicInfoTabView item={item} />}
              {activeTab === "acquisition" && (
                <AcquisitionTabView item={item} />
              )}
              {activeTab === "details" && <DetailsTabView item={item} />}
              {activeTab === "tagsSeasons" && (
                <TagsSeasonsTabView item={item} />
              )}
            </div>

            <div className="mt-6 flex justify-end gap-3">
              <button className="btn btn-primary" onClick={onEdit}>
                Edit Item
              </button>
            </div>
          </div>
        </div>
      </div>
      <div className="modal-backdrop" onClick={onClose}></div>
    </div>
  );
};
