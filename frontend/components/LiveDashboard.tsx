"use client";

import { useGoldWebSocket } from "../hooks/useGoldWebSocket";
import ConnectionStatus from "../components/ConnectionStatus";
import GoldPriceCard from "../components/GoldPriceCard";
import GoldChart from "../components/GoldChart";
import { GoldPrice, GoldHistoryResponse, GoldPricePoint } from "../types/gold";

interface Props {
    initialPrice: GoldPrice;
    initialHistory: GoldHistoryResponse;
}

export default function LiveDashboard({ initialPrice, initialHistory }: Props) {
    const { status, latestUpdate } = useGoldWebSocket();

    // Merge the live update into the price card's data, falling back to
    // server-fetched initial data until the first WS message arrives.
    const currentPrice: GoldPrice = latestUpdate
        ? {
            ...initialPrice,
            price: latestUpdate.price,
            timestamp: latestUpdate.timestamp,
        }
        : initialPrice;

    // Append the live update to the chart's history so it's visible as a
    // new point, without needing to refetch /api/gold/history.
    const history: GoldHistoryResponse = latestUpdate
        ? {
            ...initialHistory,
            data: [
                ...initialHistory.data,
                { timestamp: latestUpdate.timestamp, price: latestUpdate.price } as GoldPricePoint,
            ],
        }
        : initialHistory;

    return (
        <div>
            <ConnectionStatus status={status} />
            <GoldPriceCard price={currentPrice} />
            <GoldChart initialHistory={history} />
        </div>
    );
}