import { useState } from "react";

// Define the structure of an outfit (you can expand this later)
interface Outfit {
  id: string;
  name: string;
  items: string[]; // Array of item IDs or names
  image: string; // URL of the outfit image
}

export default function Outfits() {
  const [outfits] = useState<Outfit[]>([
    {
      id: "1",
      name: "Evening Look",
      items: ["1", "2"], // Example item IDs from your Closet
      image: "https://via.placeholder.com/600x400?text=Evening+Look",
    },
    {
      id: "2",
      name: "Casual Wear",
      items: ["1"],
      image: "https://via.placeholder.com/600x400?text=Casual+Wear",
    },
  ]);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Outfits</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {outfits.map((outfit) => (
          <div key={outfit.id} className="border rounded shadow p-4">
            <h2 className="font-semibold mb-2">{outfit.name}</h2>
            <img
              src={outfit.image}
              alt={outfit.name}
              className="w-full h-48 object-cover rounded"
            />
            <p className="mt-2">Items: {outfit.items.join(", ")}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
