import { authorized, json } from "./helpers.mjs";
export async function GET(req         ) {
  if (!authorized(req))
    return json({ error: "Sign in to search research." }, 401);
  const q = new URL(req.url).searchParams.get("q")?.trim();
  if (!q || q.length > 200)
    return json({ error: "Enter a search of 2–200 characters." }, 400);
  try {
    const u = new URL("https://api.crossref.org/works");
    u.searchParams.set("query.bibliographic", q);
    u.searchParams.set("rows", "10");
    u.searchParams.set("select", "DOI,title,author,published,abstract");
    const r = await fetch(u, {
      signal: AbortSignal.timeout(15000),
      redirect: "error",
      headers: { "User-Agent": "PatchQuestionsResearchLab/1.0" },
    });
    if (!r.ok) throw new Error();
    const d = (await r.json())       ;
    return json({
      results: (d.message?.items || []).map((x     ) => ({
        id: x.DOI,
        title: x.title?.[0] || "Untitled",
        authors: (x.author || [])
          .map((a     ) => [a.given, a.family].filter(Boolean).join(" "))
          .join(", "),
        year: x.published?.["date-parts"]?.[0]?.[0] || null,
        url: "https://doi.org/" + x.DOI,
        summary: (
          x.abstract || "Open the publisher record to inspect this work."
        )
          .replace(/<[^>]+>/g, " ")
          .replace(/\s+/g, " ")
          .slice(0, 1200),
      })),
    });
  } catch {
    return json(
      {
        error:
          "Crossref search is temporarily unavailable. Use the external search links or try again.",
      },
      502,
    );
  }
}
