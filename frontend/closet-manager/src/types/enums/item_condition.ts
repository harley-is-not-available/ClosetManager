export const ItemCondition = {
  excellent: 'excellent',
  good: 'good',
  fair: 'fair',
  poor: 'poor',
  damaged: 'damaged',
} as const;

export type ItemConditionKey = keyof typeof ItemCondition;

export type ItemConditionValue = typeof ItemCondition[ItemConditionKey];
