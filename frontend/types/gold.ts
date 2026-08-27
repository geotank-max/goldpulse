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