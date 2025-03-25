import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../api/api';
import { Link } from 'react-router-dom';

interface Application {
  id: string;
  job: {
    id: string;
    title: string;
    location: string;
    salary: string;
    description: string;
  };
  status: string;
}

export default function MyApplications() {
  const queryClient = useQueryClient();

  const { data, isLoading, error } = useQuery<Application[]>({
    queryKey: ['applications'],
    queryFn: async () => (await api.get('applications/')).data,
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => api.delete(`applications/${id}/`),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['applications'] }),
  });

  if (isLoading) return <div className="p-4 text-center">Loading your applications...</div>;
  if (error || !data) return <div className="p-4 text-center text-red-500">Failed to load applications.</div>;

  return (
    <div className="container mx-auto py-6 px-4">
      <Link to="/" className="text-blue-500 hover:underline">← Back to Jobs</Link>
      <h2 className="text-2xl font-semibold mb-4 my-3">My Applications</h2>

      {data.length === 0 ? (
        <p className="text-gray-500">You haven't applied to any jobs yet.</p>
      ) : (
        <ul className="space-y-4">
          {data.map((app) => (
            <li key={app.id} className="border p-4 rounded-lg shadow-sm">
              <Link to={`/jobs/${app.job.id}`} className="text-xl text-blue-500 hover:underline">
                {app.job.title}
              </Link>
              <p><strong>Description:</strong> {app.job.description}</p>
              <p><strong>Location:</strong> {app.job.location}</p>
              <p><strong>Salary:</strong> ${app.job.salary}</p>
              <p><strong>Status:</strong> {app.status}</p>
              <button
                onClick={() => {
                  if (window.confirm('Are you sure you want to withdraw this application?')) {
                    deleteMutation.mutate(app.id);
                  }
                }}
                className="mt-2 bg-red-500 text-white py-2 px-3 rounded"
              >
                Withdraw
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

