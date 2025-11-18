import { createSlice } from "@reduxjs/toolkit";
import type { PayloadAction } from "@reduxjs/toolkit"; // <-- Type-only import
import type { ClosetItem } from "../types/closet/closet-item";

// Initial state for clothing items
const initialState: ClosetItem[] = [
  {
    id: "1",
    brand: "Nike",
    category: "Shoes",
    color: "Black",
    size: "US 10",
    image: "https://via.placeholder.com/200x200",
  },
  {
    id: "2",
    brand: "Zara",
    category: "Dresses",
    color: "White",
    size: "XS",
    image: "https://via.placeholder.com/200x200",
  },
];

// Create the Redux slice
const itemsSlice = createSlice({
  name: "items",
  initialState,
  reducers: {
    addItem: (state, action: PayloadAction<ClosetItem>) => {
      state.push(action.payload);
    },
    removeItem: (state, action: PayloadAction<string>) => {
      return state.filter((item) => item.id !== action.payload);
    },
  },
});

// Export the reducer and actions
export const { addItem, removeItem } = itemsSlice.actions;
export default itemsSlice.reducer;
