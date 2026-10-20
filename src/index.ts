/**
 * Статический лендинг «Академия занимательных наук» — Елена Изотова.
 *
 * Файлы отдаёт биндинг ASSETS (Workers Static Assets), воркер добавляет
 * только заголовки: кэширование и базовую защиту.
 */

export interface Env {
  ASSETS: Fetcher;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const assets = env.ASSETS;
    if (!assets) {
      // Не должно случиться: биндинг объявлен в wrangler.jsonc.
      // Но 500 на каждый запрос — худший вариант, поэтому отдаём 503.
      return new Response("Static assets binding is not available.", {
        status: 503,
        headers: { "Content-Type": "text/plain; charset=utf-8" },
      });
    }

    const response = await assets.fetch(request);

    const headers = new Headers(response.headers);

    // Базовая гигиена заголовков.
    headers.set("X-Content-Type-Options", "nosniff");
    headers.set("Referrer-Policy", "strict-origin-when-cross-origin");
    headers.set("X-Frame-Options", "SAMEORIGIN");

    // HTML всегда свежий: правки текста должны появляться сразу.
    // Статика — на час, без immutable, потому что имена файлов не хэшированы.
    const isDocument = response.headers.get("Content-Type")?.includes("text/html");
    headers.set(
      "Cache-Control",
      isDocument ? "public, max-age=0, must-revalidate" : "public, max-age=3600"
    );

    return new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers,
    });
  },
};
