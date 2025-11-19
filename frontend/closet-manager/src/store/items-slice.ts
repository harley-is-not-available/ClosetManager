import { createSlice } from "@reduxjs/toolkit";
import type { PayloadAction } from "@reduxjs/toolkit";
import type { RootState } from "../../src/store";
import type { ClosetItem } from "../types/closet/closet-item";
import { fetchClothingItems } from "../utils/api";
import { createAsyncThunk } from "@reduxjs/toolkit";
import {
  LoadingStatus,
  type LoadingStatusKey,
} from "../types/enums/resource_loading_status";

export interface ClosetItemState {
  items: ClosetItem[];
  status: LoadingStatusKey;
}

// Initial state for clothing items
const initialState: ClosetItemState = {
  items: [],
  status: LoadingStatus.unloaded,
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
      state.items = state.items.filter((item) => item.id !== action.payload);
    },
    updateItem: (state, action: PayloadAction<ClosetItem>) => {
      const index = state.items.findIndex(
        (item) => item.id === action.payload.id,
      );
      if (index !== -1) {
        state.items[index] = action.payload;
      }
    },
    getItems: (state, action: PayloadAction<ClosetItem[]>) => {
      state.items = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(getItemsFromAPI.pending, (state) => {
        state.status = LoadingStatus.loading;
      })
      .addCase(getItemsFromAPI.fulfilled, (state, action) => {
        state.status = LoadingStatus.idle;
        state.items = action.payload;
      })
      .addCase(getItemsFromAPI.rejected, (state) => {
        state.status = LoadingStatus.error;
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

export const { addItem, removeItem, updateItem } = itemsSlice.actions;
export default itemsSlice.reducer;
export const selectClosetItems = (state: RootState) => state.closetItems.items;
export const selectClosetItemsStatus = (state: RootState) =>
  state.closetItems.status;
