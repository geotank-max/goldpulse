import { ConnectionState } from "../hooks/useGoldWebSocket";

interface Props {
    status: ConnectionState;
}

const STATUS_CONFIG = {
    connected: { label: "Live", color: "green" },
    connecting: { label: "Connecting...", color: "orange" },
    disconnected: { label: "Disconnected", color: "crimson" },
};

export default function ConnectionStatus({ status }: Props) {
    const { label, color } = STATUS_CONFIG[status];

    return (
        <div style={{ color, fontSize: "0.85rem" }}>
            ● {label}
        </div>
    );
}