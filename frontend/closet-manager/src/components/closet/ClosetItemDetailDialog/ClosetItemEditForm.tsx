import type { ClosetItem } from "../../../types/closet/closet-item";
import { BasicInfoTabEdit } from "./ClosetItemTabs/BasicInfoTab/BasicInfoTabEdit";
import { AcquisitionTabEdit } from "./ClosetItemTabs/AcquisitionTab/AcquisitionTabEdit";
import { TagsSeasonsTabEdit } from "./ClosetItemTabs/TagsSeasonsTab/TagsSeasonsTabEdit";
import { DetailsTabEdit } from "./ClosetItemTabs/DetailsTab/DetailsTabEdit";

interface ClosetItemEditFormProps {
  item: ClosetItem;
  errors: Record<string, string>;
  activeTab: string;
  onTabChange: (tabName: string) => void;
  onEditChange: (updatedItem: ClosetItem) => void;
  onSave: () => void;
  onCancel: () => void;
}

export const ClosetItemEditForm: React.FC<ClosetItemEditFormProps> = ({
  item,
  errors,
  activeTab,
  onTabChange,
  onEditChange,
  onSave,
  onCancel,
}) => {
  return (
    <div className="modal modal-open">
      <div className="modal-box w-11/12 max-w-5xl">
        <h3 className="text-lg font-bold">
          Edit {item.brand} - {item.category}
        </h3>

        <div className="flex flex-col md:flex-row gap-4 mt-4">
          {/* Image section */}
          <div className="w-full md:w-1/3 flex flex-col items-center justify-center">
            {/* Image upload logic would be implemented here */}
            <div className="w-full flex items-center justify-center mb-4">
              {item.image ? (
                <img
                  src={item.image}
                  alt={item.brand}
                  className="w-full max-w-xs h-48 object-cover object-center rounded-lg"
                />
              ) : (
                <div className="bg-gray-200 border-2 border-dashed rounded-xl w-full max-w-xs h-48 flex items-center justify-center">
                  <span className="text-gray-500">No Image</span>
                </div>
              )}
            </div>
          </div>

          {/* Editable fields section - tabs */}
          <div className="w-full md:w-2/3 overflow-y-auto max-h-96">
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
              {activeTab === "basicInfo" && (
                <BasicInfoTabEdit
                  item={item}
                  onChange={onEditChange}
                  errors={errors}
                />
              )}
              {activeTab === "acquisition" && (
                <AcquisitionTabEdit
                  item={item}
                  onChange={onEditChange}
                  errors={errors}
                />
              )}
              {activeTab === "details" && (
                <DetailsTabEdit
                  item={item}
                  onChange={onEditChange}
                  errors={errors}
                />
              )}
              {activeTab === "tagsSeasons" && (
                <TagsSeasonsTabEdit
                  item={item}
                  onChange={onEditChange}
                  errors={errors}
                />
              )}
            </div>

            <div className="mt-8 flex justify-end gap-3">
              <button className="btn btn-ghost" onClick={onCancel}>
                Cancel
              </button>
              <button className="btn btn-primary" onClick={onSave}>
                Save Changes
              </button>
            </div>
          </div>
        </div>
      </div>
      <div className="modal-backdrop" onClick={onCancel}></div>
    </div>
  );
};
