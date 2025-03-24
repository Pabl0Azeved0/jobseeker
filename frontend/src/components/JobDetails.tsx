import { useParams, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import api from '../api/api';

interface Job {
  id: string;
  title: string;
  description: string;
  location: string;
  salary: string;
  created_at: string;
  posted_by: string;
}

export default function JobDetails() {
  const { id } = useParams<{ id: string }>();

  const { data: job, isLoading, error } = useQuery<Job>({
    queryKey: ['job', id],
    queryFn: async () => {
      const res = await api.get(`jobs/${id}/`);
      return res.data;
    },
  });

  if (isLoading) return <div className="p-4 text-center">Loading job details...</div>;
  if (error) return <div className="p-4 text-center text-red-500">Error loading job details.</div>;

  return (
    <div className="container mx-auto py-6 px-4">
      <Link to="/" className="text-blue-500 hover:underline mb-4 inline-block">← Back to Jobs</Link>
      <h2 className="text-3xl font-semibold mb-3">{job?.title}</h2>
      <p className="mb-2"><strong>Location:</strong> {job?.location}</p>
      <p className="mb-2"><strong>Salary:</strong> ${job?.salary}</p>
      <p className="mb-2"><strong>Description:</strong></p>
      <p>{job?.description}</p>
    </div>
  );
}
