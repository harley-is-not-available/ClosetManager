export const ItemCategory = {
  top: 'top',
  bottom: 'bottom',
  dress: 'dress',
  outerwear: 'outerwear',
  shoe: 'shoe',
  accessory: 'accessory',
  lingerie: 'lingerie',
  sleepwear: 'sleepwear',
  swimsuit: 'swimsuit',
  uniform: 'uniform',
} as const;

export type ItemCategoryKey = keyof typeof ItemCategory;

export type ItemCategoryValue = typeof ItemCategory[ItemCategoryKey];
