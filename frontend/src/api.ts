const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function handleResponse(res: Response) {
  if (!res.ok) {
    let msg = res.statusText;
    try {
      const data = await res.json();
      msg = (data as any).detail || JSON.stringify(data);
    } catch {
    }
    throw new Error(msg || `HTTP ${res.status}`);
  }

  if (res.status === 204) return null;

  const contentType = res.headers.get("content-type") || "";
  if (contentType.includes("application/json")) {
    return res.json();
  }

  return res; // для FileResponse с картинкой
}

export function apiGet(path: string) {
  return fetch(`${API_URL}${path}`, {
    method: "GET",
    credentials: "include",
  }).then(handleResponse);
}

export function apiPostJson(path: string, body: any) {
  return fetch(`${API_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify(body),
  }).then(handleResponse);
}


export function apiPostForm(path: string, formData: FormData) {
  return fetch(`${API_URL}${path}`, {
    method: "POST",
    credentials: "include",
    body: formData,
  }).then(handleResponse);
}

export function apiPostVoid(path: string) {
  return fetch(`${API_URL}${path}`, {
    method: "POST",
    credentials: "include",
  }).then(handleResponse);
}
