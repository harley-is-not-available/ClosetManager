import { ItemSize, type ItemSizeKey } from "../../../types/enums/item_size";

/**
 * Component to control the size of the card in the ClosetItemTile.
 * Provides buttons for selecting between ItemSizes.
 * The currently selected size is highlighted with a primary button style.
 */
function ClosetItemTileSizeController({
  cardSize,
  handleCardSizeChange,
}: {
  /**
   * The current size of the card.
   * Can be any ItemSizeKey value
   */
  cardSize: ItemSizeKey;

  /**
   * Callback function to handle changes in card size.
   * @param size - The new size to set.
   */
  handleCardSizeChange: (size: ItemSizeKey) => void;
}) {
  return (
    <div className="mb-4 flex items-center gap-2 flex-wrap">
      <span className="text-sm font-medium">Card Size:</span>
      {(Object.keys(ItemSize) as ItemSizeKey[]).map((size) => (
        <button
          key={size}
          className={`btn btn-sm ${cardSize === size ? "btn-primary" : "btn-ghost"}`}
          onClick={() => handleCardSizeChange(size)}
        >
          {size.toUpperCase()}
        </button>
      ))}
    </div>
  );
}

export default ClosetItemTileSizeController;
