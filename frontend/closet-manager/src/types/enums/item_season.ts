export const ItemSeason = {
  spring: 'spring',
  summer: 'summer',
  fall: 'fall',
  winter: 'winter',
  allSeason: 'allSeason',
} as const;

export type ItemSeasonKey = keyof typeof ItemSeason;

export type ItemSeasonValue = typeof ItemSeason[ItemSeasonKey];
