import { useQuery } from '@tanstack/react-query';
import api from '../api/api';

interface Job {
  id: string;
  title: string;
  description: string;
  location: string;
  salary: string;
}

export default function Jobs() {
  const { data: jobs, isLoading, isError } = useQuery<Job[]>({
    queryKey: ['jobs'],
    queryFn: async () => {
      const response = await api.get<Job[]>('jobs/');
      return response.data;
    },
  });

  if (isLoading) {
    return <div className="min-h-screen flex justify-center items-center">Loading...</div>;
  }

  if (isError || !jobs) {
    return <div className="min-h-screen flex justify-center items-center text-red-500">Failed to load jobs.</div>;
  }

  return (
    <div className="max-w-3xl mx-auto py-8">
      <h1 className="text-3xl font-semibold mb-6">Job Listings</h1>
      {jobs.map((job) => (
        <div key={job.id} className="mb-4 p-4 bg-white shadow-md rounded-lg">
          <h2 className="text-xl font-semibold">{job.title}</h2>
          <p className="text-gray-700">{job.description}</p>
          <div className="mt-2 text-sm">
            <span className="font-semibold">Location:</span> {job.location}
          </div>
          <div className="text-sm">
            <span className="font-semibold">Salary:</span> ${job.salary}
          </div>
        </div>
      ))}
    </div>
  );
}
