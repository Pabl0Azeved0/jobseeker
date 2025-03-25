import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import PrivateRoute from './routes/PrivateRoute';
import Jobs from './components/Jobs';
import Signup from './components/Signup';
import { RootState } from './redux/store';
import { useSelector } from 'react-redux';
import JobDetails from './components/JobDetails';
import JobForm from './components/JobForm';
import MyApplications from './components/MyApplications';
import Profile from './pages/Profile';
import Navbar from './components/Navbar';
export default function App() {
  const { isAuthenticated } = useSelector((state: RootState) => state.auth);

  return (
    <BrowserRouter>
      {isAuthenticated && <Navbar />}
      <Routes>
        <Route path="/login" element={isAuthenticated ? <Navigate to="/" /> : <Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route element={<PrivateRoute />}>
          <Route path="/" element={<Jobs />} />
          <Route path="/jobs/:id" element={<JobDetails />} />
          <Route path="/jobs/new" element={<JobForm />} />
          <Route path="/jobs/edit/:id" element={<JobForm />} />
          <Route path="/my-applications" element={<MyApplications />} />
          <Route path="/profile" element={<Profile />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
