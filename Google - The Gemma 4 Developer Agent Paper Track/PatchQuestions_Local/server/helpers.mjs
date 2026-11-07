export function authorized() { return true; }
export function sameOrigin(req) { return !req.headers.get('origin') || req.headers.get('origin') === new URL(req.url).origin; }
export function json(data, status=200) { return Response.json(data,{status,headers:{'Cache-Control':'no-store','X-Content-Type-Options':'nosniff'}}); }
