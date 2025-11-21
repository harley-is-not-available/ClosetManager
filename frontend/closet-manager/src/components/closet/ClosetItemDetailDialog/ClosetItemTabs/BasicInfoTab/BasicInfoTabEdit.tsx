// ClosetManager/frontend/closet-manager/src/components/closet/ClosetItemDetailDialog/ClosetItemTabs/BasicInfoTab/BasicInfoTabEdit.tsx

import type { ClosetItem } from "../../../../../types/closet/closet-item";

interface BasicInfoTabEditProps {
  item: ClosetItem;
  onChange: (updatedItem: ClosetItem) => void;
  errors: Record<string, string>;
}

export const BasicInfoTabEdit = ({
  item,
  onChange,
  errors,
}: BasicInfoTabEditProps) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label className="block text-sm font-medium mb-1">Brand</label>
        <input
          type="text"
          name="brand"
          value={item.brand}
          onChange={(e) => onChange({ ...item, brand: e.target.value })}
          className={`input input-bordered w-full ${errors.brand ? "input-error" : ""}`}
          placeholder="Brand name"
        />
        {errors.brand && (
          <span className="text-error text-xs mt-1">{errors.brand}</span>
        )}
      </div>
      <div>
        <label className="block text-sm font-medium mb-1">Category</label>
        <select
          name="category"
          value={item.category}
          onChange={(e) => onChange({ ...item, category: e.target.value })}
          className={`select select-bordered w-full ${errors.category ? "select-error" : ""}`}
        >
          <option value="">Select category</option>
          <option value="tShirt">T-Shirt</option>
          <option value="jeans">Jeans</option>
          <option value="dress">Dress</option>
          <option value="jacket">Jacket</option>
          <option value="sweater">Sweater</option>
          <option value="skirt">Skirt</option>
          <option value="pants">Pants</option>
          <option value="shoes">Shoes</option>
          <option value="accessory">Accessory</option>
          <option value="other">Other</option>
        </select>
        {errors.category && (
          <span className="text-error text-xs mt-1">{errors.category}</span>
        )}
      </div>
      <div>
        <label className="block text-sm font-medium mb-1">Subcategory</label>
        <select
          name="subcategory"
          value={item.subcategory}
          onChange={(e) => onChange({ ...item, subcategory: e.target.value })}
          className="select select-bordered w-full"
        >
          <option value="">Select subcategory</option>
          <option value="tShirt">T-Shirt</option>
          <option value="sweater">Sweater</option>
          <option value="hoodie">Hoodie</option>
          <option value="jeans">Jeans</option>
          <option value="dress">Dress</option>
          <option value="skirt">Skirt</option>
          <option value="sweatpants">Sweatpants</option>
          <option value="jacket">Jacket</option>
          <option value="sneakers">Sneakers</option>
          <option value="baseballCap">Baseball Cap</option>
          <option value="winterCoat">Winter Coat</option>
          <option value="maxiSkirt">Maxi Skirt</option>
        </select>
      </div>
      <div>
        <label className="block text-sm font-medium mb-1">Color</label>
        <input
          type="text"
          name="color"
          value={item.color}
          onChange={(e) => onChange({ ...item, color: e.target.value })}
          className="input input-bordered w-full"
          placeholder="Color"
        />
      </div>
      <div>
        <label className="block text-sm font-medium mb-1">Size</label>
        <input
          type="text"
          name="size"
          value={item.size}
          onChange={(e) => onChange({ ...item, size: e.target.value })}
          className="input input-bordered w-full"
          placeholder="Size"
        />
      </div>
    </div>
  );
};
