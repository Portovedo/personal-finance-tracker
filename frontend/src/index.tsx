import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

// Remove the loading spinner
const loadingElement = document.getElementById('root');
if (loadingElement) {
  loadingElement.innerHTML = '';
}

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);