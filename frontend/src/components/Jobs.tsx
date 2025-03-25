import { useQuery } from '@tanstack/react-query';
import api from '../api/api';
import { Link } from 'react-router-dom';

interface Job {
  id: string;
  title: string;
  location: string;
  salary: string;
}

export default function Jobs() {
  const { data, isLoading, error } = useQuery<Job[]>({
    queryKey: ['jobs'],
    queryFn: async () => (await api.get('jobs/')).data,
  });

  if (isLoading) return <div className="p-4 text-center">Loading jobs...</div>;
  if (error) return <div className="p-4 text-center text-red-500">Failed to load jobs.</div>;

  return (
    <div className="container mx-auto py-6 px-4">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-semibold">Available Jobs</h2>
        <div className="flex gap-2">
          <Link
            to="/jobs/new"
            className="bg-green-500 hover:bg-green-600 text-white py-2 px-4 rounded"
          >
            + Create Job
          </Link>
          <Link
            to="/my-applications"
            className="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded"
          >
            My Applications
          </Link>
        </div>
      </div>
      <ul className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {data?.map(job => (
          <li key={job.id} className="border p-4 rounded-lg shadow-sm hover:shadow-md transition-shadow duration-300">
            <Link to={`/jobs/${job.id}`} className="block">
              <h3 className="text-xl font-medium text-blue-600">{job.title}</h3>
              <p className="text-gray-700">{job.location}</p>
              <p className="text-gray-900 font-semibold">${job.salary}</p>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
