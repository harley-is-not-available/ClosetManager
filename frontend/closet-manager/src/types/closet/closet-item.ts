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
   * The subcategory of the clothing item.
   * Example: "tShirt", "jeans", "sundress"
   */
  subcategory: string;

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

  /**
   * The source where the item was acquired.
   * Example: "Amazon", "Local Store", "Friend"
   */
  source: string;

  /**
   * The date the item was acquired.
   */
  dateAcquired: Date;

  /**
   * Indicates if the item is secondhand.
   */
  secondhand: boolean;

  /**
   * The purchase price of the item.
   */
  purchasePrice: number;

  /**
   * The original price of the item.
   */
  originalPrice: number;

  /**
   * The location where the item was purchased.
   */
  purchaseLocation: string;

  /**
   * The material of the clothing item.
   * Example: "Cotton", "Polyester", "Wool"
   */
  material: string;

  /**
   * A personal note about the item.
   */
  personalNote: string;

  /**
   * A description of the item.
   */
  description: string;

  /**
   * The condition of the item.
   * Example: "new", "likeNew", "good", "fair", "poor"
   */
  condition: string;

  /**
   * Additional details about the item's condition.
   */
  conditionDetails: string;

  /**
   * The seasons the item is suitable for.
   * Example: "spring", "summer", "fall", "winter"
   */
  seasons: string[];

  /**
   * Indicates if the item is hidden.
   */
  hidden: boolean;

  /**
   * Tags associated with the item.
   */
  tags: string[];
}
