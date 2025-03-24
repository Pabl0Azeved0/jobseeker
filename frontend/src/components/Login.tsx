import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { loginUser } from '../redux/authSlice';
import { AppDispatch, RootState } from '../redux/store';
import { Link, useNavigate } from 'react-router-dom';

export default function Login() {
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();
  const { loading, error, isAuthenticated } = useSelector((state: RootState) => state.auth);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  useEffect(() => {
    if (isAuthenticated) {
      navigate('/');
    }
  }, [isAuthenticated, navigate]);

  const handleLogin = () => {
    dispatch(loginUser({ username, password }));
  };

  const handleEnter = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') handleLogin();
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <div className="bg-white p-8 shadow-xl rounded-xl w-80">
        <h1 className="text-2xl font-semibold text-center mb-6">Login</h1>
        <input
          type="text"
          placeholder="Username"
          className="w-full mb-4 p-2 border rounded"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          className="w-full mb-4 p-2 border rounded"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          onKeyDown={handleEnter}
        />
        {error && <p className="text-red-500 text-sm mb-2">{error}</p>}
        <div className="text-center mb-4">
          <Link to="/signup" className="text-blue-500 hover:text-blue-700 underline">
            Sign Up
          </Link>
        </div>
        <button
          className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600 transition duration-200"
          onClick={handleLogin}
          disabled={loading}
        >
          {loading ? 'Logging in...' : 'Sign in'}
        </button>
      </div>
    </div>
  );
}
