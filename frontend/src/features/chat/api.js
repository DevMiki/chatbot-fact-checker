// Use relative paths by default so Vite dev proxy can forward to the backend without CORS.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

export async function send_chat_message(question, files, useLlm = true) {
  const formData = new FormData();
  formData.append('question', question);
  formData.append('use_llm', useLlm ? 'true' : 'false');
  files.forEach((file) => formData.append('files', file));
  const response = await fetch(`${API_BASE_URL}/api/chat`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || 'Request failed');
  }
  return response.json();
}
