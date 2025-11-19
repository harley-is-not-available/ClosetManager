import { useEffect, useRef, useState } from "react";
import ClosetItemListTile from "../components/closet/closet-item-list/closet-item-list-tile";
import ClosetItemListToolbar from "../components/closet/closet-item-list/closet-item-list-toolbar";
import ClosetItemTileSizeController from "../components/closet/closet-item-list/closet-item-tile-size-controller";
import { ItemSize, type ItemSizeKey } from "../types/enums/item_size";
import { useAppDispatch, useAppSelector } from "../store/redux-hooks";
import { getItemsFromAPI, selectClosetItems } from "../store/items-slice";
import ClosetItemDetailDialog from "../components/closet/ClosetItemDetailDialog";
import type { ClosetItem } from "../types/closet/closet-item";

/**
 * The main component for the Closet page.
 * This component fetches and displays clothing items, and allows the user to adjust the tile size.
 */
function Closet() {
  const dispatch = useAppDispatch();

  /**
   * State to hold the current card size.
   */
  const [cardSize, setCardSize] = useState<ItemSizeKey>("md");

  /**
   * State to hold the currently selected item for detail view.
   */
  const [selectedItem, setSelectedItem] = useState<ClosetItem | null>(null);

  /**
   * Ref to track whether the first `useEffect` has completed.
   */
  const hasLoadedFromLocalStorage = useRef(false);

  /**
   * Ref to delay the second `useEffect` until the first is done.
   */
  const isFirstLoadDone = useRef(false);

  /**
   * Effect to fetch clothing items from the API.
   * This runs once when the component mounts.
   */
  useEffect(() => {
    dispatch(getItemsFromAPI());
  }, [dispatch]);

  /**
   * Effect to read the initial card size from localStorage.
   * If no value is found in localStorage, it defaults based on screen size.
   */
  useEffect(() => {
    const savedCardSize = localStorage.getItem("closetCardSize");
    if (savedCardSize && savedCardSize in ItemSize) {
      setCardSize(savedCardSize as ItemSizeKey);
    } else {
      if (window.innerWidth < 768) {
        setCardSize("sm");
      } else {
        setCardSize("lg");
      }
    }
    hasLoadedFromLocalStorage.current = true;

    // Use a small delay to ensure the state has been updated
    const timer = setTimeout(() => {
      isFirstLoadDone.current = true;
    }, 0);

    return () => clearTimeout(timer);
  }, []);

  /**
   * Effect to save the current card size to localStorage.
   * This only runs after the first `useEffect` has completed.
   */
  useEffect(() => {
    if (isFirstLoadDone.current) {
      localStorage.setItem("closetCardSize", cardSize);
    }
  }, [cardSize, isFirstLoadDone]);

  /**
   * Handles changes to the card size.
   * @param size - The new card size to be set.
   */
  const handleCardSizeChange = (size: ItemSizeKey) => {
    setCardSize(size);
  };

  /**
   * Handles saving changes to an item.
   * @param updatedItem - The item with updated data.
   */
  const handleItemSave = (updatedItem: ClosetItem) => {
    // In a real implementation, this would update the item in the backend
    console.log("Item saved:", updatedItem);
    setSelectedItem(null);
  };

  return (
    <div className="p-6">
      <ClosetItemListToolbar onSearch={() => console.log()} />
      <ClosetItemTileSizeController
        cardSize={cardSize}
        handleCardSizeChange={handleCardSizeChange}
      />

      <div
        className={`grid-cols-[repeat(auto-fit,minmax(var(--card-size),1fr))] grid gap-2`}
        style={
          {
            "--card-size": `${ItemSize[cardSize]}px`,
          } as React.CSSProperties
        }
      >
        {useAppSelector(selectClosetItems).map((item) => (
          <ClosetItemListTile
            key={item.id}
            item={item}
            onClick={() => setSelectedItem(item)}
          />
        ))}
      </div>

      {selectedItem && (
        <ClosetItemDetailDialog
          item={selectedItem}
          onClose={() => setSelectedItem(null)}
          onSave={handleItemSave}
        />
      )}
    </div>
  );
}

export default Closet;
