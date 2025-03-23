import { Routes, Route } from 'react-router-dom';
import Login from '../components/Login';
import PrivateRoute from './PrivateRoute';
import Jobs from '../components/Jobs';

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route element={<PrivateRoute />}>
        <Route path="/" element={<Jobs />} />
      </Route>
    </Routes>
  );
}
