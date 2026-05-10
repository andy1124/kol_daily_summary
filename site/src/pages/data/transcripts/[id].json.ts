import { getAllEpisodes } from "../../../lib/data";

export function getStaticPaths() {
  return getAllEpisodes().map((ep) => ({ params: { id: ep.id } }));
}

export function GET({ params }: { params: { id: string } }) {
  const ep = getAllEpisodes().find((e) => e.id === params.id);
  return new Response(
    JSON.stringify({ transcript: ep?.transcript ?? null }),
    { headers: { "Content-Type": "application/json; charset=utf-8" } }
  );
}
