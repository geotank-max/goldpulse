import { getGoldHistory } from "../services/goldApi";
import GoldChart from "../components/GoldChart";

export default async function Home() {
  const history = await getGoldHistory("1d");

  return (
    <main style={{ padding: "2rem" }}>
      <h1>GoldPulse</h1>
      <GoldChart history={history} />
    </main>
  );
}