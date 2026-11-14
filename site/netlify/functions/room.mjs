// Хранилище залов: ПК отправляет проект, шлем загружает его по 4-значному коду.
// Данные лежат в Netlify Blobs (встроенное хранилище Netlify), поэтому ничего настраивать не нужно.
import { getStore } from "@netlify/blobs";

const H = { "content-type": "application/json; charset=utf-8", "cache-control": "no-store", "access-control-allow-origin": "*" };
const out = (obj, status = 200) => new Response(JSON.stringify(obj), { status, headers: H });

export default async (req) => {
  if (req.method === "OPTIONS") return new Response("", { headers: { ...H, "access-control-allow-methods": "GET,POST", "access-control-allow-headers": "content-type" } });
  const url = new URL(req.url);
  let code = (url.searchParams.get("code") || "").replace(/\D/g, "").slice(0, 6);
  const store = getStore({ name: "rooms", consistency: "strong" });

  if (req.method === "GET") {
    if (url.searchParams.get("ping")) return out({ ok: true, server: "netlify" });
    if (!code) return out({ ok: false, error: "не указан код зала" }, 400);
    const rec = await store.get(code, { type: "json" });
    if (!rec) return out({ ok: false, error: "зал с кодом " + code + " не найден" }, 404);
    return out({ ok: true, code, ...rec });
  }

  if (req.method === "POST") {
    let body;
    try { body = await req.json(); } catch (e) { return out({ ok: false, error: "файл проекта повреждён" }, 400); }
    const L = body && body.layout;
    if (!L || !L.hall || !Array.isArray(L.items)) return out({ ok: false, error: "это не похоже на проект зала" }, 400);
    if (JSON.stringify(L).length > 2_000_000) return out({ ok: false, error: "проект слишком большой" }, 413);
    if (!code) {
      for (let i = 0; i < 30 && !code; i++) { const c = String(1000 + Math.floor(Math.random() * 9000)); if (!(await store.get(c))) code = c; }
      if (!code) return out({ ok: false, error: "не удалось выдать код, попробуйте ещё раз" }, 500);
    }
    const rec = { layout: L, savedAt: Date.now(), items: L.items.length };
    await store.setJSON(code, rec);
    return out({ ok: true, code, savedAt: rec.savedAt, items: rec.items });
  }
  return out({ ok: false, error: "метод не поддерживается" }, 405);
};

export const config = { path: "/api/room" };
