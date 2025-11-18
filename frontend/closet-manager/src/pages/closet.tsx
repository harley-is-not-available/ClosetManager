import { useEffect, useRef, useState } from "react";
import ClosetItemListTile from "@components/closet/closet-item-list/closet-item-list-tile";
import ClosetItemListToolbar from "@components/closet/closet-item-list/closet-item-list-toolbar";
import type { ClosetItem } from "@types/closet/closet-item";
import { fetchClothingItems } from "@/src/utils/api";
import ClosetItemTileSizeController from "@components/closet/closet-item-list/closet-item-tile-size-controller";
import { ItemSize, type ItemSizeKey } from "@types/enums/item_size";

/**
 * The main component for the Closet page.
 * This component fetches and displays clothing items, and allows the user to adjust the tile size.
 */
function Closet() {
  /**
   * State to hold the list of clothing items.
   */
  const [items, setItems] = useState<ClosetItem[]>([]);

  /**
   * State to hold the current card size.
   */
  const [cardSize, setCardSize] = useState<ItemSizeKey>("md");

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
    fetchClothingItems().then(setItems);
  }, []);

  /**
   * Effect to read the initial card size from localStorage.
   * If no value is found in localStorage, it defaults based on screen size.
   */
  useEffect(() => {
    const savedCardSize = localStorage.getItem("closetCardSize");
    console.log("mounted: " + savedCardSize);
    if (savedCardSize && savedCardSize in ItemSize) {
      setCardSize(savedCardSize as ItemSizeKey);
    } else {
      console.log("made it here :(");
      if (window.innerWidth < 768) {
        setCardSize("sm");
      } else {
        setCardSize("lg");
      }
    }
    hasLoadedFromLocalStorage.current = true;
    console.log("loaded = true");

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
      console.log("saving: " + cardSize);
      localStorage.setItem("closetCardSize", cardSize);
    }
  }, [cardSize, isFirstLoadDone]);

  /**
   * Handles changes to the card size.
   * @param size - The new card size to be set.
   */
  const handleCardSizeChange = (size: ItemSizeKey) => {
    console.log("changing: " + size);
    setCardSize(size);
  };

  return (
    <div className="p-6">
      <ClosetItemListToolbar />
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
        {items.map((item) => (
          <ClosetItemListTile key={item.id} item={item} cardSize={cardSize} />
        ))}
      </div>
    </div>
  );
}

export default Closet;
