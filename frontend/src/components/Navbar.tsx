import { Link } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { logout } from '../redux/authSlice';

export default function Navbar() {
  const dispatch = useDispatch();

  const handleLogout = () => {
    dispatch(logout());
  };

  return (
    <nav className="bg-gray-800 text-white p-4">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/" className="text-xl font-bold">JobSeeker</Link>
        <div className="flex space-x-4">
          <Link to="/my-applications" className="hover:underline">My Applications</Link>
          <Link to="/profile" className="hover:underline">My Profile</Link>
          <button onClick={handleLogout} className="hover:underline">Logout</button>
        </div>
      </div>
    </nav>
  );
}
