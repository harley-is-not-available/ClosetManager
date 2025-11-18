import type { ClosetItem } from "@/types/closet/closet-item";

/**
 * A component that renders an overlay for a closet item tile.
 * This overlay is displayed on hover and contains information about the item.
 *
 * @param item - The closet item data to display in the overlay.
 * @returns - The rendered overlay component.
 */
function ClosetItemListTileOverlay({ item }: { item: ClosetItem }) {
  return (
    <div className="absolute inset-0 bg-black bg-opacity-50 opacity-0 group-hover:opacity-80 transition-opacity duration-300 flex items-center justify-center p-4 z-10">
      <div className="text-white text-sm backdrop-blur-sm rounded-lg p-3 bg-black bg-opacity-30">
        <div className="font-semibold">{item.brand}</div>
        <div className="text-xs opacity-80 mt-1">
          {item.category} - {item.color} ({item.size})
        </div>
      </div>
    </div>
  );
}

export default ClosetItemListTileOverlay;
