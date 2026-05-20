// All network calls in one place so tests have one thing to mock.
const BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000';

export async function listTasks()         { return (await fetch(`${BASE}/tasks`)).json(); }
export async function createTask(input)   { return (await fetch(`${BASE}/tasks`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(input) })).json(); }
export async function patchTask(id, p)    { return (await fetch(`${BASE}/tasks/${id}`, { method: 'PATCH', headers: { 'content-type': 'application/json' }, body: JSON.stringify(p) })).json(); }
export async function deleteTask(id)      { return fetch(`${BASE}/tasks/${id}`, { method: 'DELETE' }); }
