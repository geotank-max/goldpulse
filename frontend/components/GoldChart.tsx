"use client";

import { useState, useEffect } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { GoldHistoryResponse } from "../types/gold";
import { getGoldHistory } from "../services/goldApi";

interface Props {
  initialHistory: GoldHistoryResponse;
}

const RANGES = ["1d", "1w", "1m", "3m", "6m", "1y"];

export default function GoldChart({ initialHistory }: Props) {
  const [range, setRange] = useState("1d");
  const [history, setHistory] = useState(initialHistory);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (range === "1d") return; // already have initial data for 1d, skip refetch on mount

    let cancelled = false;
    setLoading(true);

    getGoldHistory(range).then((data) => {
      if (!cancelled) {
        setHistory(data);
        setLoading(false);
      }
    });

    return () => {
      cancelled = true;
    };
  }, [range]);

  const chartData = history.data.map((point) => ({
    time: new Date(point.timestamp).toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    }),
    price: point.price,
  }));

  return (
    <div>
      <div style={{ display: "flex", gap: "0.5rem", marginBottom: "1rem" }}>
        {RANGES.map((r) => (
          <button
            key={r}
            onClick={() => setRange(r)}
            style={{
              fontWeight: r === range ? 700 : 400,
              textTransform: "uppercase",
            }}
          >
            {r}
          </button>
        ))}
      </div>

      {loading && <div>Loading...</div>}

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <XAxis dataKey="time" />
          <YAxis domain={["auto", "auto"]} />
          <Tooltip />
          <Line type="monotone" dataKey="price" stroke="#d4af37" dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}