import { useParams, Link, useNavigate } from 'react-router-dom';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import api from '../api/api';

export default function JobDetails() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const { data: job, isLoading, error } = useQuery({
    queryKey: ['job', id],
    queryFn: async () => (await api.get(`jobs/${id}/`)).data,
  });

  const handleDelete = async () => {
    if (confirm('Are you sure you want to delete this job?')) {
      await api.delete(`jobs/${id}/`);
      queryClient.invalidateQueries({ queryKey: ['jobs'] });
      navigate('/');
    }
  };

  const handleEdit = async () => {
    navigate(`/jobs/edit/${job.id}`);
  }

  const applyMutation = useMutation({
    mutationFn: async () => {
      const response = await api.post('applications/', { job_id: id, status: 'applied' });
      return response.data;
    },
    onSuccess: () => {
      alert('Successfully applied!');
      queryClient.invalidateQueries({ queryKey: ['applications'] });
    },
    onError: (error: any) => {
      if (error.response?.status === 400) {
        alert('You have already applied to this job.');
      } else {
        alert('Application failed, please try again.');
      }
    },
  });

  const handleApply = () => applyMutation.mutate();

  if (isLoading) return <div className="p-4">Loading...</div>;
  if (error) return <div className="p-4 text-red-500">Error loading job details.</div>;

  return (
    <div className="container mx-auto py-6 px-4">
      <Link to="/" className="text-blue-500 hover:underline">← Back to Jobs</Link>
      <h2 className="text-3xl font-semibold my-3">{job.title}</h2>
      <p className="mb-2"><strong>Location:</strong> {job.location}</p>
      <p className="mb-2"><strong>Salary:</strong> ${job.salary}</p>
      <p className="mb-4">{job.description}</p>
      <div>
        <div className='mb-1'>
          <button onClick={handleApply} className='bg-green-500 text-white py-3 px-12 rounded'>
            Apply
          </button>
        </div>
        <button onClick={handleEdit} className="bg-blue-500 text-white py-2 px-4 rounded mr-1">Edit</button>
        <button onClick={handleDelete} className="bg-red-500 text-white py-2 px-4 rounded">Delete</button>
      </div>
    </div>
  );
}
