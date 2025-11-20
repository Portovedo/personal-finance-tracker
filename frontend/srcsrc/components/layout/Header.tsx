
import React from 'react';
import { useAuth } from '../../contexts/AuthContext';

const Header = () => {
    const { logout } = useAuth();

    return (
        <header className="bg-white shadow p-4 flex justify-between items-center">
            <h1 className="text-xl font-bold">Dashboard</h1>
            <button onClick={logout} className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">
                Logout
            </button>
        </header>
    );
};

export default Header;
