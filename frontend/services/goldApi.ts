const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function getGoldHistory(range: string = "1d") {
  const res = await fetch(`${API_URL}/api/gold/history?range_=${range}`, {
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch gold history: ${res.status}`);
  }

  return res.json();
}

export async function getCurrentPrice() {
  const res = await fetch(`${API_URL}/api/gold/current`, {
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch current price: ${res.status}`);
  }

  return res.json();
}

export async function getStatistics() {
  const res = await fetch(`${API_URL}/api/gold/statistics`, {
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch statistics: ${res.status}`);
  }

  return res.json();
}