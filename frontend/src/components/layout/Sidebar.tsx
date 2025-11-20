import React from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import {
  HomeIcon,
  CreditCardIcon,
  BanknotesIcon,
  FolderIcon,
  ChartBarIcon,
  DocumentTextIcon,
  CogIcon,
  ArrowRightOnRectangleIcon,
} from '@heroicons/react/24/outline';

const Sidebar: React.FC = () => {
  const { user, logout } = useAuth();
  const location = useLocation();

  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: HomeIcon },
    { name: 'Accounts', href: '/accounts', icon: CreditCardIcon },
    { name: 'Transactions', href: '/transactions', icon: BanknotesIcon },
    { name: 'Categories', href: '/categories', icon: FolderIcon },
    { name: 'Portfolio', href: '/portfolio', icon: ChartBarIcon },
    { name: 'Statements', href: '/statements', icon: DocumentTextIcon },
    { name: 'Analytics', href: '/analytics', icon: ChartBarIcon },
    { name: 'Settings', href: '/settings', icon: CogIcon },
  ];

  return (
    <div className="hidden md:flex md:w-64 md:flex-col">
      {/* Sidebar component, swap this element with another sidebar if you like */}
      <div className="flex flex-col flex-grow bg-white border-r border-gray-200 pt-5 pb-4 overflow-y-auto">
        <div className="flex items-center flex-shrink-0 px-4">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="h-8 w-8 bg-primary-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">F</span>
              </div>
            </div>
            <div className="ml-3">
              <h1 className="text-xl font-bold text-gray-900">FinanceTracker</h1>
            </div>
          </div>
        </div>

        {/* User profile */}
        <div className="mt-8 px-4">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="h-10 w-10 bg-gray-300 rounded-full flex items-center justify-center">
                {user?.full_name ? (
                  <span className="text-gray-600 font-medium">
                    {user.full_name.split(' ').map(n => n[0]).join('').toUpperCase()}
                  </span>
                ) : (
                  <span className="text-gray-600 font-medium">
                    {user?.email?.[0]?.toUpperCase()}
                  </span>
                )}
              </div>
            </div>
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-900">
                {user?.full_name || user?.email}
              </p>
              <p className="text-xs text-gray-500">Premium Plan</p>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="mt-8 flex-1 px-2 space-y-1">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href;
            return (
              <NavLink
                key={item.name}
                to={item.href}
                className={`group flex items-center px-2 py-2 text-sm font-medium rounded-md transition-colors duration-150 ${
                  isActive
                    ? 'bg-primary-50 text-primary-700 border-r-2 border-primary-700'
                    : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                }`}
              >
                <item.icon
                  className={`mr-3 flex-shrink-0 h-5 w-5 ${
                    isActive ? 'text-primary-700' : 'text-gray-400 group-hover:text-gray-500'
                  }`}
                  aria-hidden="true"
                />
                {item.name}
              </NavLink>
            );
          })}
        </nav>

        {/* Logout */}
        <div className="px-2 mt-auto">
          <button
            onClick={logout}
            className="group flex items-center px-2 py-2 text-sm font-medium text-gray-600 rounded-md hover:bg-gray-50 hover:text-gray-900 transition-colors duration-150 w-full"
          >
            <ArrowRightOnRectangleIcon
              className="mr-3 flex-shrink-0 h-5 w-5 text-gray-400 group-hover:text-gray-500"
              aria-hidden="true"
            />
            Logout
          </button>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;