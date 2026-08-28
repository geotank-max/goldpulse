import { GoldStatistics as GoldStatisticsType } from "../types/gold";

interface Props {
  stats: GoldStatisticsType;
}

export default function GoldStatistics({ stats }: Props) {
  const items = [
    { label: "High", value: stats.high },
    { label: "Low", value: stats.low },
    { label: "Open", value: stats.open },
  ];

  return (
    <div style={{ display: "flex", gap: "2rem", marginTop: "1.5rem" }}>
      {items.map((item) => (
        <div key={item.label}>
          <div style={{ color: "#888", fontSize: "0.85rem" }}>{item.label}</div>
          <div style={{ fontWeight: 600 }}>${item.value.toFixed(2)}</div>
        </div>
      ))}
    </div>
  );
}