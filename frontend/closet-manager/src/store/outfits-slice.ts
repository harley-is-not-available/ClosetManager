import { createSlice } from "@reduxjs/toolkit";
import type { PayloadAction } from "@reduxjs/toolkit"; // <-- Type-only import

// Define the structure of an outfit
interface Outfit {
  id: string;
  name: string;
  items: string[];
  image: string;
}

// Initial state for outfits
const initialState: Outfit[] = [];

// Create the Redux slice
const outfitsSlice = createSlice({
  name: "outfits",
  initialState,
  reducers: {
    addOutfit: (state, action: PayloadAction<Outfit>) => {
      state.push(action.payload);
    },
  },
});

// Export the reducer and actions
export default outfitsSlice.reducer;
