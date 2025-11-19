export const ItemSubcategory = {
  // Tops
  tShirt: 'tShirt',
  poloShirt: 'poloShirt',
  blouse: 'blouse',
  shirt: 'shirt',
  sweater: 'sweater',
  jacket: 'jacket',
  hoodie: 'hoodie',
  tankTop: 'tankTop',
  cropTop: 'cropTop',
  bodice: 'bodice',
  vest: 'vest',

  // Bottoms
  jeans: 'jeans',
  pants: 'pants',
  skirt: 'skirt',
  shorts: 'shorts',
  trousers: 'trousers',
  capris: 'capris',
  leggings: 'leggings',
  sweatpants: 'sweatpants',

  // Dresses
  sundress: 'sundress',
  cocktailDress: 'cocktailDress',
  eveningDress: 'eveningDress',
  partyDress: 'partyDress',
  workDress: 'workDress',
  casualDress: 'casualDress',

  // Outerwear
  coat: 'coat',
  parka: 'parka',
  trenchCoat: 'trenchCoat',
  windbreaker: 'windbreaker',
  cardigan: 'cardigan',
  blazer: 'blazer',

  // Shoes
  sneakers: 'sneakers',
  boots: 'boots',
  sandals: 'sandals',
  heels: 'heels',
  flats: 'flats',
  loafers: 'loafers',
  ankleBoots: 'ankleBoots',
  hikingBoots: 'hikingBoots',

  // Accessories
  hat: 'hat',
  scarf: 'scarf',
  gloves: 'gloves',
  belt: 'belt',
  jewelry: 'jewelry',
  sunglasses: 'sunglasses',
  wallet: 'wallet',
  bag: 'bag',

  // Lingerie
  bra: 'bra',
  panties: 'panties',
  robe: 'robe',
  negligee: 'negligee',
  camisole: 'camisole',

  // Sleepwear
  pajamas: 'pajamas',
  nightgown: 'nightgown',
  sleepShirt: 'sleepShirt',

  // Swimsuit
  bikini: 'bikini',
  onePiece: 'onePiece',
  swimShorts: 'swimShorts',
  rashGuard: 'rashGuard',

  // Uniform
  schoolUniform: 'schoolUniform',
  workUniform: 'workUniform',
  militaryUniform: 'militaryUniform',
  sportsUniform: 'sportsUniform',
} as const;

export type ItemSubcategoryKey = keyof typeof ItemSubcategory;

export type ItemSubcategoryValue = typeof ItemSubcategory[ItemSubcategoryKey];
