import React from 'react';
import { Link } from 'react-router-dom';

const RegisterPage = () => (
  <div className="flex justify-center items-center h-screen bg-gray-100">
    <div className="p-8 bg-white rounded shadow">
      <h1 className="text-2xl mb-4">Register</h1>
      <p>Registration coming soon.</p>
      <Link to="/login" className="text-blue-600">Back to Login</Link>
    </div>
  </div>
);
export default RegisterPage;