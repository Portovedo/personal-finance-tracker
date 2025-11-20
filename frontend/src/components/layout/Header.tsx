import React from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { useTheme } from '../../contexts/ThemeContext';
import {
  BellIcon,
  MagnifyingGlassIcon,
  SunIcon,
  MoonIcon,
} from '@heroicons/react/24/outline';

const Header: React.FC = () => {
  const { user } = useAuth();
  const { theme, setTheme, resolvedTheme } = useTheme();

  const toggleTheme = () => {
    setTheme(theme === 'light' ? 'dark' : 'light');
  };

  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Search bar */}
          <div className="flex-1 flex items-center">
            <div className="max-w-lg w-full lg:max-w-xs">
              <label htmlFor="search" className="sr-only">
                Search
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <MagnifyingGlassIcon
                    className="h-5 w-5 text-gray-400"
                    aria-hidden="true"
                  />
                </div>
                <input
                  id="search"
                  name="search"
                  className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                  placeholder="Search transactions, accounts..."
                  type="search"
                />
              </div>
            </div>
          </div>

          {/* Right side */}
          <div className="ml-4 flex items-center md:ml-6 space-x-4">
            {/* Theme toggle */}
            <button
              onClick={toggleTheme}
              className="p-2 rounded-full text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              {resolvedTheme === 'dark' ? (
                <SunIcon className="h-5 w-5" aria-hidden="true" />
              ) : (
                <MoonIcon className="h-5 w-5" aria-hidden="true" />
              )}
              <span className="sr-only">Toggle theme</span>
            </button>

            {/* Notifications */}
            <button className="p-2 rounded-full text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
              <BellIcon className="h-5 w-5" aria-hidden="true" />
              <span className="sr-only">View notifications</span>
            </button>

            {/* Profile dropdown */}
            <div className="relative">
              <div className="flex items-center">
                <div className="h-8 w-8 bg-gray-300 rounded-full flex items-center justify-center">
                  {user?.full_name ? (
                    <span className="text-gray-600 font-medium text-sm">
                      {user.full_name.split(' ').map(n => n[0]).join('').toUpperCase()}
                    </span>
                  ) : (
                    <span className="text-gray-600 font-medium text-sm">
                      {user?.email?.[0]?.toUpperCase()}
                    </span>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;