import shirt from "../assets/orange-tshirt.png";
import type { ClosetItem } from "../types/closet/closet-item";
import type { ItemCategoryKey } from "../types/enums/item_category";
import type { ItemConditionKey } from "../types/enums/item_condition";
import type { ItemSeasonKey } from "../types/enums/item_season";
import type { ItemSubcategoryKey } from "../types/enums/item_subcategory";

// Add mock upload function for image uploads
export async function mockUploadImage(file: File): Promise<string> {
  // Simulate network delay to mimic real API behavior
  await new Promise((resolve) =>
    setTimeout(resolve, 1000 + Math.random() * 1000),
  );

  // Convert file to data URL
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result as string);
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

export async function fetchClothingItems(): Promise<ClosetItem[]> {
  const brands = [
    "Adidas",
    "Zara",
    "Nike",
    "H&M",
    "Puma",
    "Uniqlo",
    "Gap",
    "Forever 21",
  ];
  const categories = [
    "Shoes",
    "Dresses",
    "T-Shirts",
    "Jeans",
    "Hats",
    "Sweaters",
    "Coats",
    "Skirts",
  ];
  const subcategories = [
    "sneakers",
    "sundress",
    "tShirt",
    "jeans",
    "baseballCap",
    "hoodie",
    "winterCoat",
    "maxiSkirt",
  ];
  const colors = [
    "White",
    "Black",
    "Red",
    "Blue",
    "Green",
    "Yellow",
    "Gray",
    "Purple",
  ];
  const sizes = ["US 9", "XS", "Large", "US 8", "S", "M", "US 10", "XXL"];
  const sources = ["Amazon", "Local Store", "Friend", "Online", "Thrift Store"];
  const materials = [
    "Cotton",
    "Polyester",
    "Wool",
    "Silk",
    "Linen",
    "Denim",
    "Nylon",
    "Rayon",
  ];
  const conditions = ["new", "likeNew", "good", "fair", "poor"];
  const seasons = ["spring", "summer", "fall", "winter"];

  const items: ClosetItem[] = [];
  for (let i = 1; i <= 64; i++) {
    const randomBrand = brands[Math.floor(Math.random() * brands.length)];
    const randomCategory = categories[
      Math.floor(Math.random() * categories.length)
    ] as ItemCategoryKey;
    const randomSubcategory = subcategories[
      Math.floor(Math.random() * subcategories.length)
    ] as ItemSubcategoryKey;
    const randomColor = colors[Math.floor(Math.random() * colors.length)];
    const randomSize = sizes[Math.floor(Math.random() * sizes.length)];
    const randomSource = sources[Math.floor(Math.random() * sources.length)];
    const randomMaterial =
      materials[Math.floor(Math.random() * materials.length)];
    const randomCondition = conditions[
      Math.floor(Math.random() * conditions.length)
    ] as ItemConditionKey;
    const randomSeasons = [
      seasons[Math.floor(Math.random() * seasons.length)] as ItemSeasonKey,
      seasons[Math.floor(Math.random() * seasons.length)] as ItemSeasonKey,
    ];

    const randomWidth = Math.floor(Math.random() * 500) + 100;
    const randomHeight = Math.floor(Math.random() * 500) + 100;

    let image = undefined;
    const randomImageChance = Math.random();

    if (randomImageChance < 0.05) {
      image = undefined;
    } else if (randomImageChance < 0.1) {
      image = "uhoh";
    } else if (randomImageChance < 0.2) {
      image = shirt;
    } else {
      image = `https://picsum.photos/${randomWidth}/${randomHeight}`;
    }

    // Generate random dates within the last 5 years
    const dateAcquired = new Date();
    dateAcquired.setDate(
      dateAcquired.getDate() - Math.floor(Math.random() * 1825),
    );

    // Generate random prices
    const purchasePrice = Math.floor(Math.random() * 200) + 10;
    const originalPrice = purchasePrice + Math.floor(Math.random() * 100);

    // Generate random tags
    const tags = ["favourite", "casual", "work", "outdoor", "formal", "summer"];
    const randomTags = [
      tags[Math.floor(Math.random() * tags.length)],
      tags[Math.floor(Math.random() * tags.length)],
    ];

    items.push({
      id: i.toString(),
      brand: randomBrand,
      category: randomCategory,
      subcategory: randomSubcategory,
      color: randomColor,
      size: randomSize,
      image: image,
      source: randomSource,
      dateAcquired: dateAcquired,
      secondhand: Math.random() > 0.5,
      purchasePrice: purchasePrice,
      originalPrice: originalPrice,
      purchaseLocation: "Unknown Location",
      material: randomMaterial,
      personalNote: `Personal note for item ${i}`,
      description: `Description for ${randomBrand} ${randomCategory} item`,
      condition: randomCondition,
      conditionDetails: "No specific details",
      seasons: randomSeasons,
      hidden: Math.random() > 0.8,
      tags: randomTags,
    });
  }

  return items;
}
