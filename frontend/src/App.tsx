import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Login from './components/Login';
import PrivateRoute from './routes/PrivateRoute';
import Jobs from './components/Jobs';
import Signup from './components/Signup';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />

        <Route element={<PrivateRoute />}>
          <Route path="/" element={<Jobs />} />
        </Route>
        <Route path="/signup" element={<Signup />} />
      </Routes>
    </BrowserRouter>
  );
}
