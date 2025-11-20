import React from 'react';
import { Outlet, Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const Layout = () => {
  const { logout } = useAuth();

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <aside className="w-64 bg-white shadow-md hidden md:block">
        <div className="p-4 font-bold text-xl border-b">Finance Tracker</div>
        <nav className="p-4 space-y-2">
          <Link to="/" className="block p-2 hover:bg-gray-100 rounded">Dashboard</Link>
          <Link to="/transactions" className="block p-2 hover:bg-gray-100 rounded">Transactions</Link>
          <Link to="/accounts" className="block p-2 hover:bg-gray-100 rounded">Accounts</Link>
          <Link to="/portfolio" className="block p-2 hover:bg-gray-100 rounded">Portfolio</Link>
          <Link to="/reports" className="block p-2 hover:bg-gray-100 rounded">Reports</Link>
          <Link to="/settings" className="block p-2 hover:bg-gray-100 rounded">Settings</Link>
        </nav>
        <div className="p-4 border-t">
            <button onClick={logout} className="text-red-600">Logout</button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-auto p-8">
        <Outlet />
      </main>
    </div>
  );
};

export default Layout;