import type { ClosetItem } from "../../../types/closet/closet-item";
import { useState } from "react";
import { ClosetItemView } from "./ClosetItemView";
import { ClosetItemEditForm } from "./ClosetItemEditForm";

interface ClosetItemDetailDialogProps {
  item: ClosetItem;
  onClose: () => void;
  onSave: (updatedItem: ClosetItem) => void;
  isEditing?: boolean;
}

export const ClosetItemDetailDialog: React.FC<ClosetItemDetailDialogProps> = ({
  item,
  onClose,
  onSave,
  isEditing: initialIsEditing = false,
}) => {
  const [isEditing, setIsEditing] = useState(initialIsEditing);
  const [editedItem, setEditedItem] = useState<ClosetItem>(item);
  const [activeTab, setActiveTab] = useState<string>("basicInfo");
  const [errors, setErrors] = useState<Record<string, string>>({});

  // Handle save logic
  const handleSave = () => {
    // Validation logic: required fields are brand, category, image
    const newErrors: Record<string, string> = {};

    // Required field validation
    if (!editedItem.brand.trim()) {
      newErrors.brand = "Brand is required";
    }
    if (!editedItem.category.trim()) {
      newErrors.category = "Category is required";
    }
    if (!editedItem.image) {
      newErrors.image = "Image is required";
    }

    setErrors(newErrors);

    // Only save if no required field errors
    if (Object.keys(newErrors).length === 0) {
      onSave(editedItem);
      setIsEditing(false);
    }
  };

  // Handle cancel logic
  const handleCancel = () => {
    setEditedItem(item);
    setErrors({});
    setIsEditing(false);
    onClose();
  };

  // Handle tab change
  const handleTabChange = (tabName: string) => {
    setActiveTab(tabName);
  };

  // Render based on mode
  if (isEditing) {
    return (
      <ClosetItemEditForm
        item={editedItem}
        errors={errors}
        activeTab={activeTab}
        onTabChange={handleTabChange}
        onEditChange={setEditedItem}
        onSave={handleSave}
        onCancel={handleCancel}
      />
    );
  }

  return (
    <ClosetItemView
      item={item}
      activeTab={activeTab}
      onTabChange={handleTabChange}
      onEdit={() => setIsEditing(true)}
      onClose={onClose}
    />
  );
};
