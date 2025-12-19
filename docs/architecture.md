# Architecture overview

## Components
- Frontend: Vite + React UI in `frontend/`. Talks to the backend via a proxy so the browser avoids CORS issues.
- Backend: FastAPI app in `backend/app/`. Handles validation, file saving, caching, and mock responses.
- Cache: Redis (in-memory data store) via the `redis` service. If Redis is unreachable, the backend switches to an in-memory cache automatically.
- Storage: PDFs saved to `data/uploads` (created on startup). System PDFs live in `data/system_files` and are auto-generated if missing.

## Runtime topology (Docker Compose)
- Frontend: http://localhost:5173 (proxy forwards `/api` to `http://backend:8000` inside the Compose network).
- Backend: http://127.0.0.1:8000 exposed from the `backend` service.
- Redis: localhost port 6379 exposed from the `redis` service.

## Request/response flow
1) User enters a question and optionally attaches PDFs in the React UI.
2) Frontend sends a `multipart/form-data` POST to `/api/chat` through the Vite proxy (proxy: forwards browser `/api` calls to the backend).
3) Backend validates inputs: question present, PDFs only, each under `MAX_UPLOAD_MB` (10 MB default).
4) Backend saves each PDF to `UPLOAD_DIR` with a sanitized, unique filename and hashes the content (SHA-256).
5) Cache key = normalized question (lowercase, trimmed) + sorted file hashes. Backend checks Redis first, then falls back to the in-memory cache if Redis is down.
6) If cache hit: return stored response with `cache_hit: true`.
7) If miss: build a mock answer and collect file references (uploaded files + up to two system files), then cache the response.
8) Frontend shows the answer. A "Related files / Fact-check" toggle reveals the filenames and whether they came from uploads or system files.

## Where key logic lives
- API surface: `backend/app/features/chat/routes.py`, `backend/app/features/health/routes.py`
- Startup + system file generation: `backend/app/main.py`, `backend/app/features/chat/correlation.py`
- Chat orchestration and caching: `backend/app/features/chat/service.py`
- File validation, hashing, and storage: `backend/app/features/chat/storage.py`
- Correlation logic + system files: `backend/app/features/chat/correlation.py`
- Cache implementations: `backend/app/cache/redis_cache.py`, `backend/app/cache/in_memory.py`, factory in `backend/app/cache/__init__.py`
- Frontend main UI: `frontend/src/app/App.jsx`
- Frontend chat form + messages: `frontend/src/features/chat/components/ChatInput.jsx`, `frontend/src/features/chat/components/ChatMessage.jsx`, `frontend/src/features/chat/components/RelatedFilesList.jsx`
- Frontend API helpers: `frontend/src/features/chat/api.js`, `frontend/src/features/health/api.js`
- Frontend UI helpers: `frontend/src/shared/ui/index.js`
- Proxy config: `frontend/vite.config.js`
