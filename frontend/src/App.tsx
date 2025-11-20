import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'react-hot-toast';
import { AuthProvider } from './contexts/AuthContext';
import { ThemeProvider } from './contexts/ThemeContext';
import ProtectedRoute from './components/auth/ProtectedRoute';
import Layout from './components/layout/Layout';

// Pages
import LoginPage from './pages/auth/LoginPage';
import RegisterPage from './pages/auth/RegisterPage';
import DashboardPage from './pages/dashboard/DashboardPage';
import AccountsPage from './pages/accounts/AccountsPage';
import TransactionsPage from './pages/transactions/TransactionsPage';
import CategoriesPage from './pages/categories/CategoriesPage';
import PortfolioPage from './pages/portfolio/PortfolioPage';
import StatementsPage from './pages/statements/StatementsPage';
import AnalyticsPage from './pages/analytics/AnalyticsPage';
import SettingsPage from './pages/settings/SettingsPage';
import NotFoundPage from './pages/errors/NotFoundPage';
import ReportsPage from './pages/reports/ReportsPage';

// Create React Query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <AuthProvider>
          <Router>
            <div className="App">
              <Routes>
                {/* Public routes */}
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />

                {/* Protected routes */}
                <Route
                  path="/*"
                  element={
                    <ProtectedRoute>
                      <Layout>
                        <Routes>
                          <Route path="/" element={<Navigate to="/dashboard" replace />} />
                          <Route path="/dashboard" element={<DashboardPage />} />
                          <Route path="/accounts" element={<AccountsPage />} />
                          <Route path="/accounts/:id" element={<AccountsPage />} />
                          <Route path="/transactions" element={<TransactionsPage />} />
                          <Route path="/transactions/:id" element={<TransactionsPage />} />
                          <Route path="/categories" element={<CategoriesPage />} />
                          <Route path="/categories/:id" element={<CategoriesPage />} />
                          <Route path="/portfolio" element={<PortfolioPage />} />
                          <Route path="/portfolio/:id" element={<PortfolioPage />} />
                          <Route path="/statements" element={<StatementsPage />} />
                          <Route path="/statements/:id" element={<StatementsPage />} />
                          <Route path="/analytics" element={<AnalyticsPage />} />
                          <Route path="/reports" element={<ReportsPage />} />
                          <Route path="/settings" element={<SettingsPage />} />
                          <Route path="*" element={<NotFoundPage />} />
                        </Routes>
                      </Layout>
                    </ProtectedRoute>
                  }
                />
              </Routes>

              {/* Global toast notifications */}
              <Toaster
                position="top-right"
                toastOptions={{
                  duration: 4000,
                  style: {
                    background: '#363636',
                    color: '#fff',
                  },
                  success: {
                    duration: 3000,
                    iconTheme: {
                      primary: '#22c55e',
                      secondary: '#fff',
                    },
                  },
                  error: {
                    duration: 5000,
                    iconTheme: {
                      primary: '#ef4444',
                      secondary: '#fff',
                    },
                  },
                }}
              />
            </div>
          </Router>
        </AuthProvider>
      </ThemeProvider>
    </QueryClientProvider>
  );
}

export default App;