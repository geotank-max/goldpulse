"use client";

import { useEffect, useRef, useState } from "react";

export type ConnectionState = "connecting" | "connected" | "disconnected";

interface GoldPriceUpdate {
    type: string;
    symbol: string;
    price: number;
    timestamp: string;
}

export function useGoldWebSocket() {
    const [status, setStatus] = useState<ConnectionState>("connecting");
    const [latestUpdate, setLatestUpdate] = useState<GoldPriceUpdate | null>(null);
    const wsRef = useRef<WebSocket | null>(null);
    const reconnectTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

    useEffect(() => {
        let isUnmounted = false;

        function connect() {
            const wsUrl = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000/ws/gold";
            const ws = new WebSocket(wsUrl);
            wsRef.current = ws;
            setStatus("connecting");

            ws.onopen = () => {
                setStatus("connected");
            };

            ws.onmessage = (event) => {
                const data: GoldPriceUpdate = JSON.parse(event.data);
                setLatestUpdate(data);
            };

            ws.onclose = () => {
                if (isUnmounted) return;
                setStatus("disconnected");
                reconnectTimeoutRef.current = setTimeout(connect, 3000);
            };

            ws.onerror = () => {
                ws.close();
            };
        }

        connect();

        return () => {
            isUnmounted = true;
            if (reconnectTimeoutRef.current) clearTimeout(reconnectTimeoutRef.current);
            wsRef.current?.close();
        };
    }, []);

    return { status, latestUpdate };
}