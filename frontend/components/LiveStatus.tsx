"use client";

import { useGoldWebSocket } from "../hooks/useGoldWebSocket";
import ConnectionStatus from "../components/ConnectionStatus";

export default function LiveStatus() {
    const { status } = useGoldWebSocket();
    return <ConnectionStatus status={status} />;
}