import { getGoldHistory, getCurrentPrice } from "../services/goldApi";
import GoldChart from "../components/GoldChart";
import GoldPriceCard from "../components/GoldPriceCard";

export default async function Home() {
  const [history, currentPrice] = await Promise.all([
    getGoldHistory("1d"),
    getCurrentPrice(),
  ]);

  return (
    <main style={{ padding: "2rem" }}>
      <h1>GoldPulse</h1>
      <GoldPriceCard price={currentPrice} />
      <GoldChart history={history} />
    </main>
  );
}