import { useEffect, useState } from 'react';
import { listTasks, createTask, patchTask, deleteTask } from './api.js';

export default function App() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState('');

  async function refresh() { setTasks(await listTasks()); }
  useEffect(() => { refresh(); }, []);

  async function add(e) {
    e.preventDefault();
    if (!title.trim()) return;
    await createTask({ title });
    setTitle('');
    refresh();
  }

  return (
    <main style={{ fontFamily: 'system-ui', maxWidth: 480, margin: '2rem auto' }}>
      <h1>Tasks</h1>
      <form onSubmit={add} style={{ display: 'flex', gap: 8 }}>
        <input value={title} onChange={e => setTitle(e.target.value)}
               placeholder="What needs doing?" style={{ flex: 1, padding: 8 }} />
        <button type="submit">Add</button>
      </form>
      <ul>
        {tasks.map(t => (
          <li key={t.id} style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <input type="checkbox" checked={t.done}
                   onChange={() => patchTask(t.id, { done: !t.done }).then(refresh)} />
            <span style={{ textDecoration: t.done ? 'line-through' : 'none', flex: 1 }}>
              {t.title}
            </span>
            <button onClick={() => deleteTask(t.id).then(refresh)}>×</button>
          </li>
        ))}
      </ul>
    </main>
  );
}
