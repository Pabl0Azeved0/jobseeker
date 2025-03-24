import { useState, useEffect } from 'react';
import { useNavigate, useParams, Link } from 'react-router-dom';
import api from '../api/api';

export default function JobForm() {
  const navigate = useNavigate();
  const { id } = useParams<{ id?: string }>();
  const editing = Boolean(id);

  const [form, setForm] = useState({
    title: '',
    description: '',
    location: '',
    salary: '',
  });

  useEffect(() => {
    if (editing) {
      api.get(`jobs/${id}/`).then(res => setForm(res.data));
    }
  }, [id, editing]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editing) {
        await api.put(`jobs/${id}/`, form);
        navigate(`/jobs/${id}`);
      } else {
        await api.post('jobs/', form);
        navigate('/');
      }
    } catch {
      alert('Failed to save job.');
    }
  };

  return (
    <div className="container mx-auto py-6 px-4">
      {editing && (
        <Link to={`/jobs/${id}`} className="text-blue-500 hover:underline inline-block mb-4">
          ← Back to Job
        </Link>
      )}
      <h2 className="text-2xl font-semibold mb-4">{editing ? 'Edit Job' : 'Create Job'}</h2>
      <form onSubmit={handleSubmit}>
        <input
          required
          name="title"
          value={form.title}
          onChange={handleChange}
          placeholder="Title"
          className="mb-3 w-full p-2 border rounded"
        />
        <textarea
          required
          name="description"
          value={form.description}
          onChange={handleChange}
          placeholder="Description"
          className="mb-3 w-full p-2 border rounded"
        />
        <input
          required
          name="location"
          value={form.location}
          onChange={handleChange}
          placeholder="Location"
          className="mb-3 w-full p-2 border rounded"
        />
        <input
          required
          name="salary"
          value={form.salary}
          onChange={handleChange}
          placeholder="Salary"
          className="mb-3 w-full p-2 border rounded"
        />
        <button type="submit" className="bg-green-500 hover:bg-green-600 text-white py-2 px-4 rounded">
          {editing ? 'Update Job' : 'Create Job'}
        </button>
        <button
        type="button"
        onClick={() => navigate(editing ? `/jobs/${id}` : '/')}
        className="bg-red-500 hover:bg-red-600 text-white py-2 px-4 rounded ml-1"
        >
          Cancel
        </button>
      </form>
    </div>
  );
}
