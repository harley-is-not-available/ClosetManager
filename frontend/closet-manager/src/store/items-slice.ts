import { createSlice } from "@reduxjs/toolkit";
import type { PayloadAction } from "@reduxjs/toolkit";
import type { AppThunk, RootState } from "../../src/store";
import type { ClosetItem } from "../types/closet/closet-item";
import { fetchClothingItems } from "../utils/api";
import { createAsyncThunk } from "@reduxjs/toolkit";

export interface ClosetItemState {
  items: ClosetItem[];
  status: "idle" | "loading" | "failed";
}

// Initial state for clothing items
const initialState: ClosetItemState = {
  items: [],
  status: "idle",
};

// Create the Redux slice
const itemsSlice = createSlice({
  name: "closetItems",
  initialState,
  reducers: {
    addItem: (state, action: PayloadAction<ClosetItem>) => {
      state.items.push(action.payload);
    },
    removeItem: (state, action: PayloadAction<string>) => {
      state.items.filter((item) => item.id !== action.payload);
    },
    getItems: (state, action: PayloadAction<ClosetItem[]>) => {
      state.items = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      // Handle the action types defined by the `incrementAsync` thunk defined below.
      // This lets the slice reducer update the state with request status and results.
      .addCase(getItemsFromAPI.pending, (state) => {
        state.status = "loading";
      })
      .addCase(getItemsFromAPI.fulfilled, (state, action) => {
        state.status = "idle";
        state.items = action.payload;
      })
      .addCase(getItemsFromAPI.rejected, (state) => {
        state.status = "failed";
      });
  },
});

export const getItemsFromAPI = createAsyncThunk(
  "closetItems/fetchItems",
  async () => {
    const items = await fetchClothingItems();
    return items;
  },
);

// Export the reducer and actions
export const { addItem, removeItem, getItems } = itemsSlice.actions;
export default itemsSlice.reducer;
export const selectClosetItems = (state: RootState) => state.closetItems.items;
