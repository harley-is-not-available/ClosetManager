/**
 * Represents a clothing item in the application.
 * This interface is used to define the structure of clothing data across the app.
 */
export interface ClosetItem {
  /**
   * Unique identifier for the clothing item.
   * This is typically used for database references or key lookups.
   */
  id: string;

  /**
   * The brand of the clothing item.
   * Example: "Nike", "Zara", "Uniqlo"
   */
  brand: string;

  /**
   * The category of the clothing item.
   * Example: "T-Shirt", "Jeans", "Dress"
   */
  category: string;

  /**
   * The color of the clothing item.
   * Example: "Black", "Blue", "White"
   */
  color: string;

  /**
   * The size of the clothing item.
   * Example: "S", "M", "L", "XL", "US-9"
   */
  size: string;

  /**
   * The image URL associated with the clothing item.
   * Can be `undefined` if no image is available.
   */
  image: string | undefined;
}
