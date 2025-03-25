import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../api/api';
import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

interface Profile {
  id: string;
  bio: string;
  skills: string;
  contact: string;
}

export default function Profile() {
  const queryClient = useQueryClient();

  const { data: profile, isLoading, error } = useQuery<Profile>({
    queryKey: ['profile'],
    queryFn: async () => (await api.get('profiles/me/')).data,
  });

  const updateMutation = useMutation({
    mutationFn: (updatedProfile: Partial<Profile>) => api.put(`profiles/${profile?.id}/`, updatedProfile),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['profile'] });
      alert('Profile updated successfully!');
    },
  });

  const [bio, setBio] = useState('');
  const [skills, setSkills] = useState('');
  const [contact, setContact] = useState('');

  useEffect(() => {
    if (profile) {
      setBio(profile.bio);
      setSkills(profile.skills);
      setContact(profile.contact);
    }
  }, [profile]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    updateMutation.mutate({ bio, skills, contact });
  };

  if (isLoading) return <div className="p-4">Loading profile...</div>;
  if (error || !profile) return <div className="p-4 text-red-500">Failed to load profile.</div>;

  return (
    <div className="container mx-auto py-6 px-4">
      <Link to="/" className="text-blue-500 hover:underline">← Back to Jobs</Link>
      <h2 className="text-2xl font-semibold mb-4 my-3">My Profile</h2>

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

        <button type="submit" className="bg-blue-500 text-white py-2 px-4 rounded">
          Update Profile
        </button>
      </form>
    </div>
  );
}
