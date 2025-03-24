import { useState } from 'react';
import api from '../api/api';
import { Link, useNavigate } from 'react-router-dom';

export default function Signup() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    username: '',
    email: '',
    password: '',
    password2: '',
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const validatePassword = (password: string) => {
    const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*]).{8,}$/;
    return regex.test(password);
  };

  const handleSignup = async () => {
    setError('');
    if (!validatePassword(form.password)) {
      setError('Password must have at least 8 chars, include upper and lowercase letters, numbers, and special chars.');
      return;
    }
    if (form.password !== form.password2) {
      setError('Passwords do not match.');
      return;
    }
    if (!form.email.includes('@')) {
      setError('Provide a valid email.');
      return;
    }
    if (form.username.length < 3) {
      setError('Username must have at least 3 characters.');
      return;
    }
  
    try {
      await api.post('signup/', form);
      setSuccess('Signup successful! Redirecting to login...');
      setTimeout(() => navigate('/login'), 2000);
    } catch (err: any) {
      const backendError = err.response?.data;
      if (backendError?.username) {
        setError(backendError.username[0]);
      } else if (backendError?.email) {
        setError(backendError.email[0]);
      } else if (backendError?.password) {
        setError(backendError.password[0]);
      } else {
        setError('Signup failed.');
      }
    }
  };  

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <div className="bg-white p-8 shadow-xl rounded-xl w-96">
        <h1 className="text-2xl font-semibold text-center mb-6">Sign Up</h1>
        <input
          placeholder="Username"
          className="w-full mb-3 p-2 border rounded"
          onChange={(e) => setForm({ ...form, username: e.target.value })}
        />
        <input
          type="email"
          placeholder="Email"
          className="w-full mb-3 p-2 border rounded"
          onChange={(e) => setForm({ ...form, email: e.target.value })}
        />
        <input
          type="password"
          placeholder="Password"
          className="w-full mb-3 p-2 border rounded"
          onChange={(e) => setForm({ ...form, password: e.target.value })}
        />
        <input
          type="password"
          placeholder="Confirm Password"
          className="w-full mb-4 p-2 border rounded"
          onChange={(e) => setForm({ ...form, password2: e.target.value })}
        />
        {error && <p className="text-red-500 text-sm mb-2">{error}</p>}
        {success && <p className="text-green-500 text-sm mb-2">{success}</p>}
        <button
          className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600 transition duration-200 mb-1"
          onClick={handleSignup}
        >
          Sign Up
        </button>
        <Link to={"/login"} className='w-full rounded py-2 block text-white text-center bg-red-500 hover:bg-red-600'>
          Back to Login
        </Link>
      </div>
    </div>
  );
}
