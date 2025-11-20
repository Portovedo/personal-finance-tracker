import React from 'react';

const AccountsPage = () => {
  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Accounts</h1>
      <div className="bg-white p-6 rounded-lg shadow-md">
        <p className="text-gray-600">Your connected bank accounts will appear here.</p>
        <button className="mt-4 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
          Add Manual Account
        </button>
      </div>
    </div>
  );
};

export default AccountsPage;