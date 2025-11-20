import React from 'react';

const DashboardPage = () => {
  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white p-4 rounded shadow">
          <h3 className="font-bold text-gray-500">Total Balance</h3>
          <p className="text-2xl">$0.00</p>
        </div>
      </div>
    </div>
  );
};
export default DashboardPage;