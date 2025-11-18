import {
  configureStore,
  type Action,
  type ThunkAction,
} from "@reduxjs/toolkit";
import closetItemsReducer from "./items-slice";
import outfitsReducer from "./outfits-slice";

export const store = configureStore({
  reducer: {
    closetItems: closetItemsReducer,
    outfits: outfitsReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
export type AppStore = typeof store;
// Define a reusable type describing thunk functions
export type AppThunk<ThunkReturnType = void> = ThunkAction<
  ThunkReturnType,
  RootState,
  unknown,
  Action
>;
