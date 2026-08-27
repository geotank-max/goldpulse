import { GoldPrice } from "../types/gold";

interface Props {
  price: GoldPrice;
}

export default function GoldPriceCard({ price }: Props) {
  const isUp = price.change >= 0;

  return (
    <div style={{ marginBottom: "1.5rem" }}>
      <div style={{ fontSize: "2.5rem", fontWeight: 700 }}>
        ${price.price.toFixed(2)}
      </div>
      <div style={{ color: isUp ? "green" : "crimson" }}>
        {isUp ? "+" : ""}
        {price.change.toFixed(2)} ({isUp ? "+" : ""}
        {price.change_percent.toFixed(2)}%)
      </div>
      <div style={{ color: "#888", fontSize: "0.85rem" }}>
        {price.symbol} · Last updated:{" "}
        {new Date(price.timestamp).toLocaleTimeString()}
      </div>
    </div>
  );
}