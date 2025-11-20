
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { PieChart, Pie, Cell, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

const DashboardPage = () => {
  const [summary, setSummary] = useState(null);

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const response = await axios.get('/api/v1/dashboard/summary');
        setSummary(response.data);
      } catch (error) {
        console.error('Error fetching dashboard summary:', error);
      }
    };
    fetchSummary();
  }, []);

  if (!summary) {
    return <div>Loading...</div>;
  }

  const assetAllocationData = Object.entries(summary.asset_allocation).map(([name, value]) => ({ name, value }));

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <h2 className="text-xl font-bold">Net Worth: ${summary.net_worth}</h2>
        </div>
        <div>
          <h2 className="text-xl font-bold">Asset Allocation</h2>
          <PieChart width={400} height={400}>
            <Pie
              data={assetAllocationData}
              cx={200}
              cy={200}
              labelLine={false}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
            >
              {assetAllocationData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </div>
        <div className="md:col-span-2">
          <h2 className="text-xl font-bold">Portfolio Value Over Time</h2>
          <LineChart
            width={800}
            height={400}
            data={summary.portfolio_value_over_time}
            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="value" stroke="#8884d8" activeDot={{ r: 8 }} />
          </LineChart>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
