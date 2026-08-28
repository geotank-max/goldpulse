export interface GoldPricePoint {
  timestamp: string;
  price: number;
}

export interface GoldHistoryResponse {
  symbol: string;
  unit: string;
  currency: string;
  data: GoldPricePoint[];
}

export interface GoldPrice {
  symbol: string;
  price: number;
  change: number;
  change_percent: number;
  timestamp: string;
}

export interface GoldStatistics {
  symbol: string;
  high: number;
  low: number;
  open: number;
  current: number;
  change_percent: number;
}