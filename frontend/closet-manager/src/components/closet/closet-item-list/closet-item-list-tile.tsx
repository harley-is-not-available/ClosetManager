import type { ClosetItem } from "@/types/closet/closet-item";
import ClosetItemListTileOverlay from "@components/closet/closet-item-list/closet-item-list-tile-overlay";
import { useState } from "react";

/**
 * Renders a single tile in the closet item list.
 * Each tile displays an image of the item and an overlay with additional details.
 *
 * @param item - The closet item data to display
 * @returns The rendered tile component
 */
function ClosetItemListTile({ item }: { item: ClosetItem }) {
  // Track whether the image is valid (to handle cases where the image URL is broken)
  const [isImageValid, setIsImageValid] = useState(true);

  return (
    <div className={`relative group`}>
      <div className="card bg-base-100 bg-linear-to-br from-base-200 to-base-300 shadow-md hover:shadow-lg transition-all duration-300 rounded-xl overflow-hidden">
        <div className="aspect-4/3 relative">
          {/* Display the item image if it exists and is valid */}
          {item.image != undefined && isImageValid ? (
            <img
              src={item.image}
              alt={item.brand}
              className="w-full h-full object-cover"
              // Handle image errors by marking the image as invalid
              onError={() => setIsImageValid(false)}
            />
          ) : (
            // Fallback UI if the image is missing or invalid
            <div className="w-full h-full flex items-center justify-center text-base-content/50">
              <span className="text-lg font-medium">No Image</span>
            </div>
          )}
          {/* Overlay component to display additional item details */}
          <ClosetItemListTileOverlay item={item} />
        </div>
      </div>
    </div>
  );
}

export default ClosetItemListTile;
