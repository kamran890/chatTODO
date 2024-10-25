import { BrowserRouter, Routes, Route, Navigate, } from 'react-router-dom';

import Login from './pages/Login';
import Dashboard from './pages/Dashboard';

function App() {
  return (
    <BrowserRouter basename="/" >
      <Routes >
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login/" element={<Login />} />
        <Route path="/dashboard/" element={<Dashboard />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;