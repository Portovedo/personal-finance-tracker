
import React from 'react';
import { Link } from 'react-router-dom';

const Sidebar = () => {
    return (
        <div className="w-64 bg-gray-800 text-white h-screen">
            <div className="p-4">
                <h2 className="text-2xl font-bold">Finance Tracker</h2>
            </div>
            <nav>
                <ul>
                    <li className="p-4 hover:bg-gray-700"><Link to="/dashboard">Dashboard</Link></li>
                    <li className="p-4 hover:bg-gray-700"><Link to="/accounts">Accounts</Link></li>
                    <li className="p-4 hover:bg-gray-700"><Link to="/transactions">Transactions</Link></li>
                    <li className="p-4 hover:bg-gray-700"><Link to="/statements">Statements</Link></li>
                    <li className="p-4 hover:bg-gray-700"><Link to="/portfolio">Portfolio</Link></li>
                    <li className="p-4 hover:bg-gray-700"><Link to="/reports">Reports</Link></li>
                    <li className="p-4 hover:bg-gray-700"><Link to="/settings">Settings</Link></li>
                </ul>
            </nav>
        </div>
    );
};

export default Sidebar;
