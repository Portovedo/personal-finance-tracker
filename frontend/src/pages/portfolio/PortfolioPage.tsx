import React from 'react';
import PlaidLink from '../../components/portfolio/PlaidLink';

const PortfolioPage = () => {
  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Portfolio</h1>
        <PlaidLink />
      </div>
      <p>No holdings found.</p>
    </div>
  );
};
export default PortfolioPage;