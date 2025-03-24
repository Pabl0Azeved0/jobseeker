import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import PrivateRoute from './routes/PrivateRoute';
import Jobs from './components/Jobs';
import Signup from './components/Signup';
import { RootState } from './redux/store';
import { useSelector } from 'react-redux';
import JobDetails from './components/JobDetails';
import JobForm from './components/JobForm';

export default function App() {
  const { isAuthenticated } = useSelector((state: RootState) => state.auth);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={isAuthenticated ? <Navigate to="/" /> : <Login />} />
        <Route element={<PrivateRoute />}>
          <Route path="/" element={isAuthenticated ? <Jobs /> : <Navigate to="/login" />} />
        </Route>
        <Route path="/signup" element={<Signup />} />
        <Route path="/jobs/:id" element={isAuthenticated ? <JobDetails /> : <Navigate to="/login" />} />
        <Route path="/jobs/new" element={isAuthenticated ? <JobForm /> : <Navigate to="/login" />} />
        <Route path="/jobs/edit/:id" element={isAuthenticated ? <JobForm /> : <Navigate to="/login" />} />
      </Routes>
    </BrowserRouter>
  );
}
