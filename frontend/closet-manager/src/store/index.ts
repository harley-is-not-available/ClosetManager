import { configureStore } from "@reduxjs/toolkit";
import itemsReducer from "./items-slice";
import outfitsReducer from "./outfits-slice";

export const store = configureStore({
  reducer: {
    items: itemsReducer,
    outfits: outfitsReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
