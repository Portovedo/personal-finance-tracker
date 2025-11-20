
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import CreatePortfolio from '../../components/portfolio/CreatePortfolio';
import AddHolding from '../../components/portfolio/AddHolding';
import PlaidLink from '../../components/portfolio/PlaidLink';

const PortfolioPage = () => {
  const { portfolioId } = useParams();
  const [portfolio, setPortfolio] = useState(null);

  useEffect(() => {
    const fetchPortfolio = async () => {
      try {
        const response = await axios.get(`/api/v1/portfolio/${portfolioId}`);
        setPortfolio(response.data);
      } catch (error) {
        console.error('Error fetching portfolio:', error);
      }
    };

    if (portfolioId) {
      fetchPortfolio();
    }
  }, [portfolioId]);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Portfolio</h1>
      {!portfolioId && <CreatePortfolio />}
      {portfolio && (
        <div>
          <h2 className="text-xl font-bold">{portfolio.name}</h2>
          <AddHolding portfolioId={portfolioId} />
          <PlaidLink />
          <table className="min-w-full bg-white mt-4">
            <thead>
              <tr>
                <th className="py-2">Symbol</th>
                <th className="py-2">Quantity</th>
                <th className="py-2">Average Cost</th>
                <th className="py-2">Current Price</th>
                <th className="py-2">Current Value</th>
              </tr>
            </thead>
            <tbody>
              {portfolio.holdings.map(holding => (
                <tr key={holding.id}>
                  <td className="border px-4 py-2">{holding.symbol}</td>
                  <td className="border px-4 py-2">{holding.quantity}</td>
                  <td className="border px-4 py-2">{holding.avg_cost}</td>
                  <td className="border px-4 py-2">{holding.current_price}</td>
                  <td className="border px-4 py-2">{holding.current_value}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default PortfolioPage;
