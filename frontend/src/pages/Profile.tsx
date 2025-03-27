import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../api/api';
import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

interface Profile {
  id: string;
  bio: string;
  skills?: string;
  contact?: string;
  resume?: string;
}

export default function Profile() {
  const queryClient = useQueryClient();

  const { data: profile, isLoading, error } = useQuery<Profile>({
    queryKey: ['profile'],
    queryFn: async () => (await api.get('profiles/me/')).data,
  });

  const updateMutation = useMutation({
    mutationFn: (updatedProfile: FormData) =>
      api.put(`/profiles/me/`, updatedProfile, { headers: { 'Content-Type': 'multipart/form-data' } }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['profile'] });
    },
  });

  const [bio, setBio] = useState('');
  const [skills, setSkills] = useState('');
  const [contact, setContact] = useState('');
  const [resume, setResume] = useState<File | null>(null);
  const [feedback, setFeedback] = useState({ message: '', type: '' });

  useEffect(() => {
    if (profile) {
      setBio(profile.bio);
      setSkills(profile.skills || '');
      setContact(profile.contact || '');
    }
  }, [profile]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const formData = new FormData();
  
    formData.append('bio', bio || '');
    formData.append('skills', skills || '');
    formData.append('contact', contact || '');
  
    if (resume) {
      formData.append('resume', resume);
    }
  
    updateMutation.mutate(formData, {
      onSuccess: () => {
        setFeedback({ message: 'Profile updated successfully!', type: 'success' });
        setTimeout(() => setFeedback({ message: '', type: '' }), 3000);
      },
      onError: (error) => {
        console.error(error);
        setFeedback({ message: 'Failed to update profile.', type: 'error' });
        setTimeout(() => setFeedback({ message: '', type: '' }), 3000);
      }
    });
  };  

  if (isLoading || updateMutation.isPending) {
    return (
      <div className="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-50 z-50">
        <div className="bg-white p-6 rounded-lg shadow-lg flex flex-col items-center">
          <svg className="animate-spin h-10 w-10 text-blue-500 mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor"
              d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z">
            </path>
          </svg>
          <span className="text-gray-700 font-medium text-lg">Loading your profile...</span>
        </div>
      </div>
    );
  }

  if (error || !profile) return <div className="p-4 text-red-500">Failed to load profile.</div>;

  return (
    <div className="container mx-auto py-6 px-4">
      <Link to="/" className="text-blue-500 hover:underline">
        ← Back to Jobs
      </Link>
      <h2 className="text-2xl font-semibold mb-4 my-3">My Profile</h2>

      {feedback.message && (
        <div className={`my-3 p-3 rounded ${feedback.type === 'success' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
          {feedback.message}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block">Bio:</label>
          <textarea
            value={bio}
            onChange={(e) => setBio(e.target.value)}
            className="w-full border rounded p-2"
            rows={4}
          />
        </div>

        <div>
          <label className="block">Skills:</label>
          <input
            type="text"
            value={skills}
            onChange={(e) => setSkills(e.target.value)}
            className="w-full border rounded p-2"
          />
        </div>

        <div>
          <label className="block">Contact:</label>
          <input
            type="text"
            value={contact}
            onChange={(e) => setContact(e.target.value)}
            className="w-full border rounded p-2"
          />
        </div>

        <div>
          <label className="block">Resume:</label>
          <input type="file" onChange={(e) => setResume(e.target.files?.[0] || null)} className="mt-2" />
          {profile.resume && (
            <p className="mt-2">
              Current Resume:{' '}
              <a
                href={profile.resume}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-500 hover:underline"
              >
                {decodeURIComponent(profile.resume.split('/').pop() || 'View Resume')}
              </a>
            </p>
          )}
        </div>

        <button type="submit" className="bg-blue-500 text-white py-2 px-4 rounded">
          Update Profile
        </button>
      </form>
    </div>
  );
}
