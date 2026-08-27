import { getGoldHistory } from "../services/goldApi";

export default async function Home() {
  const history = await getGoldHistory("1d");

  return (
    <main>
      <h1>GoldPulse</h1>
      <pre>{JSON.stringify(history, null, 2)}</pre>
    </main>
  );
}