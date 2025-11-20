import React from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

const LoginPage = () => {
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleLogin = () => {
    // Mock login
    login('mock-token', 'mock-refresh');
    navigate('/');
  };

  return (
    <div className="flex justify-center items-center h-screen bg-gray-100">
      <div className="bg-white p-8 rounded shadow-md">
        <h1 className="text-2xl mb-4">Login</h1>
        <button onClick={handleLogin} className="bg-blue-600 text-white px-4 py-2 rounded">
          Sign In (Demo)
        </button>
      </div>
    </div>
  );
};

export default LoginPage;