# API

Base URL in Docker: http://127.0.0.1:8000
Base URL in dev (Vite proxy): use relative `/api` from http://localhost:5173.

## Health
- `GET /api/health`
- Response: `{"status":"ok"}`

## Chat
- `POST /api/chat`
- Content type: `multipart/form-data` (format that mixes text fields and file uploads).
- Fields:
  - `question` (string, required)
  - `files` (0..n PDFs)
- Success response body:
```json
{
  "answer": "Mock answer for: Hello?",
  "referenced_files": [
    {"name": "file1.pdf", "source": "uploaded"},
    {"name": "company_policy.pdf", "source": "system"}
  ],
  "cache_hit": false
}
```
- Notes:
  - Size limit: default 10 MB per file (`MAX_UPLOAD_MB`).
  - Accepted type: PDF only (checks `.pdf` extension).
  - Cache key: normalized question + hashes of uploaded files; Redis first, then memory fallback.

### Examples
Health check:
```bash
curl http://127.0.0.1:8000/api/health
```

Ask without files:
```bash
curl -X POST -F "question=What is the policy?" http://127.0.0.1:8000/api/chat
```