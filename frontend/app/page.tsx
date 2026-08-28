import { getGoldHistory, getCurrentPrice, getStatistics } from "../services/goldApi";
import GoldChart from "../components/GoldChart";
import GoldPriceCard from "../components/GoldPriceCard";
import GoldStatistics from "../components/GoldStatistics";

export default async function Home() {
  const [history, currentPrice, stats] = await Promise.all([
    getGoldHistory("1d"),
    getCurrentPrice(),
    getStatistics(),
  ]);

  return (
    <main style={{ padding: "2rem" }}>
      <h1>GoldPulse</h1>
      <GoldPriceCard price={currentPrice} />
      <GoldChart initialHistory={history} />
      <GoldStatistics stats={stats} />
    </main>
  );
}