import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Closet from "./pages/closet.tsx";
import Outfits from "./pages/outfits.tsx";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Closet />,
  },
  {
    path: "/outfits",
    element: <Outfits />,
  },
]);

export default function Routes() {
  return <RouterProvider router={router} />;
}
