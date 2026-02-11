# ⚽ Football Game Tracker - Azure Web App
# Wander Self-Hosted (WanderTross-style)
Self-hosted photo travel blog with synced map view, smooth scroll feed, and keyword-aware map.

## Stack
- Backend: Node + Express + SQLite, blurhash placeholders
- Frontend: Vite + React + TypeScript + MapLibre + Tailwind
- Docker: compose with frontend + backend

## Quickstart (local)
1) Backend
```bash
cd backend
cp .env.example .env
npm install
npm run seed
npm run dev
```
2) Frontend
```bash
cd frontend
npm install
npm run dev
```
Frontend runs on 5173 (proxied to backend 4000).

## Docker
```bash
docker compose up --build
```
Frontend exposed on 5173, backend 4000.

## Data model
- posts: id, title, body, photo_url, lat/lng, city/country, keywords, blurhash, created_at

## API
- GET /api/posts — list posts
- GET /api/posts/:id — fetch one
- POST /api/posts — create (title, body, photo_url required; optional lat/lng/city/country/keywords[])
- PUT /api/posts/:id — update
- DELETE /api/posts/:id — delete

## Frontend behavior
- Scroll feed with snap + map sync; hovering or entering a card pans map to marker
- Map click selects post
- Lazy-loaded images
- Keyword chips shown per post (future: filter)

## Env
- backend/.env: PORT, CLIENT_ORIGIN
- frontend: uses Vite proxy in dev; set VITE_API_BASE for deployed reverse proxy

## Seed
`npm run seed` in backend inserts 3 sample posts with geotags and remote photos.

## Next steps
- Add keyword-based clustering/overlay on map
- Add upload UI and drag/drop photo URL input
- Add tests + lint
