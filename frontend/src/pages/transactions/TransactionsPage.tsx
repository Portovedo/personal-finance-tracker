
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

const TransactionsPage = () => {
  const { accountId } = useParams();
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    const fetchTransactions = async () => {
      try {
        const response = await axios.get(`/api/v1/transactions/${accountId}`);
        setTransactions(response.data);
      } catch (error) {
        console.error('Error fetching transactions:', error);
      }
    };

    if (accountId) {
      fetchTransactions();
    }
  }, [accountId]);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Transactions</h1>
      <table className="min-w-full bg-white">
        <thead>
          <tr>
            <th className="py-2">Date</th>
            <th className="py-2">Description</th>
            <th className="py-2">Amount</th>
            <th className="py-2">Category</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map(transaction => (
            <tr key={transaction.id}>
              <td className="border px-4 py-2">{new Date(transaction.transaction_date).toLocaleDateString()}</td>
              <td className="border px-4 py-2">{transaction.description}</td>
              <td className="border px-4 py-2">{transaction.amount}</td>
              <td className="border px-4 py-2">{transaction.category?.name || 'Uncategorized'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TransactionsPage;
