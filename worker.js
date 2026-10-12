// Worker: /api/count -> D1 (binding DB); semua path lain -> aset statis.
const INIT = "CREATE TABLE IF NOT EXISTS counter (id TEXT PRIMARY KEY, n INTEGER NOT NULL DEFAULT 0)";
const H = { "content-type": "application/json", "cache-control": "no-store" };
const json = (o, s = 200) => new Response(JSON.stringify(o), { status: s, headers: H });
async function count(db) {
  const r = await db.prepare("SELECT n FROM counter WHERE id = 'hitung'").first();
  return r ? r.n : 0;
}
export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (url.pathname === "/api/count") {
      if (!env.DB) return json({ error: "no-db" }, 503);
      await env.DB.prepare(INIT).run();
      if (req.method === "POST") {
        await env.DB.prepare("INSERT INTO counter (id, n) VALUES ('hitung', 1) ON CONFLICT(id) DO UPDATE SET n = n + 1").run();
      } else if (req.method !== "GET") return json({ error: "method" }, 405);
      return json({ count: await count(env.DB) });
    }
    return env.ASSETS.fetch(req);
  }
};
