
import React from 'react';
import { render, screen } from '@testing-library/react';
import StatementsPage from './StatementsPage';

test('renders statements page', () => {
  render(<StatementsPage />);
  const linkElement = screen.getByText(/Upload Statement/i);
  expect(linkElement).toBeInTheDocument();
});
