# Troubleshooting

## Ports already in use
- Frontend uses 5173, backend uses 8000, Redis uses 6379. Stop anything on those ports or change the exposed ports in `docker-compose.yml` and match them in Vite config if needed. (You can easily kill a port with "npx kill-port port_number")

## Proxy issues
- Vite proxy forwards `/api` to `BACKEND_PROXY_TARGET`. Defaults: `http://127.0.0.1:8000` in dev; `http://backend:8000` in Docker Compose via `docker-compose.yml`.
- If API calls fail from the browser in dev, confirm `BACKEND_PROXY_TARGET` points to the backend URL you are running.

## Redis down
- The backend logs a warning and falls back to the in-memory cache automatically. No action needed unless you require Redis persistence; then restart the Redis service and the backend container.

## CORS errors
- The UI uses the proxy so the browser avoids CORS. If you hit the backend directly from a different origin without the proxy, you may see CORS blocks; use the proxy or add CORS handling to the backend (not included in this MVP).

## Stale build
- If frontend assets talk to an older backend in Docker, rebuild with:
```
docker compose up --build
```
