"use client";

import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { GoldHistoryResponse } from "../types/gold";

interface Props {
  history: GoldHistoryResponse;
}

export default function GoldChart({ history }: Props) {
  const chartData = history.data.map((point) => ({
    time: new Date(point.timestamp).toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    }),
    price: point.price,
  }));

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={chartData}>
        <XAxis dataKey="time" />
        <YAxis domain={["auto", "auto"]} />
        <Tooltip />
        <Line type="monotone" dataKey="price" stroke="#d4af37" dot={false} />
      </LineChart>
    </ResponsiveContainer>
  );
}