import type { ClosetItem } from "../../../types/closet/closet-item";

/**
 * A component that renders an overlay for a closet item tile.
 * This overlay is displayed on hover and contains information about the item.
 *
 * @param item - The closet item data to display in the overlay.
 * @returns - The rendered overlay component.
 */
function ClosetItemListTileOverlay({ item }: { item: ClosetItem }) {
  return (
    <div className="absolute inset-0 bg-base-100 bg-opacity-70 opacity-0 group-hover:opacity-90 transition-opacity duration-300 flex items-center justify-center p-4 z-10">
      <div className="text-base-content text-sm backdrop-blur-sm rounded-lg p-4 bg-base-200 bg-opacity-60 w-full max-w-xs">
        <div className="font-semibold text-center">{item.brand}</div>
        <div className="text-xs opacity-90 mt-2 text-center">
          <p>
            {item.category} - {item.subcategory}
          </p>
          <p>
            {item.color} ({item.size})
          </p>
        </div>
      </div>
    </div>
  );
}

export default ClosetItemListTileOverlay;
