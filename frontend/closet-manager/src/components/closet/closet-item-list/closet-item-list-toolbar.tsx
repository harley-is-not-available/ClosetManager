import { Cog6ToothIcon } from "@heroicons/react/24/solid";
import { useState } from "react";

/**
 * A toolbar component for the Closet Item List, providing search functionality
 * and a settings button.
 *
 * @param onSearch - A callback function that is triggered when the search query changes.
 *                   The function receives the current search query as a string.
 */
function ClosetItemListToolbar({
  onSearch,
}: {
  onSearch: (query: string) => void;
}) {
  /**
   * State variable to hold the current search query.
   */
  const [searchQuery, setSearchQuery] = useState("");

  /**
   * Handles the search input change, updating the searchQuery state
   * and invoking the onSearch callback with the new query.
   *
   * @param query - The new search query string.
   */
  const handleSearch = (query: string) => {
    setSearchQuery(query);
    onSearch(query);
  };

  return (
    <div className="flex items-center gap-3 pb-4">
      <div className="flex-1 min-w-0">
        <div className="form-control">
          <div className="input-group">
            <input
              type="text"
              placeholder="Search items..."
              className="input input-bordered w-full"
              value={searchQuery}
              onChange={(e) => handleSearch(e.target.value)}
            />
            <button className="btn btn-square btn-ghost">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-5 w-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>
      <button
        className="btn btn-ghost btn-circle"
        onClick={() => {
          console.log("Settings button pressed");
        }}
      >
        <Cog6ToothIcon className="h-6 w-6" />
      </button>
    </div>
  );
}

export default ClosetItemListToolbar;
