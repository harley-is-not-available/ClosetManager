import shirt from "../assets/orange-tshirt.png";

export async function fetchClothingItems() {
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

  const items = [];
  for (let i = 1; i <= 64; i++) {
    const randomBrand = brands[Math.floor(Math.random() * brands.length)];
    const randomCategory =
      categories[Math.floor(Math.random() * categories.length)];
    const randomColor = colors[Math.floor(Math.random() * colors.length)];
    const randomSize = sizes[Math.floor(Math.random() * sizes.length)];
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

    items.push({
      id: i.toString(),
      brand: randomBrand,
      category: randomCategory,
      color: randomColor,
      size: randomSize,
      image: image,
    });
  }

  return items;
}
