import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import { UserProvider } from './context/UserContext'; // Context provider for user data

// Initialize the root element and render the React application
const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <React.StrictMode>
    {/* Wrap the app with UserProvider to manage global user state */}
    <UserProvider>
      {/* Enable routing for the application */}
      <BrowserRouter>
        {/* Render the main App component */}
        <App />
      </BrowserRouter>
    </UserProvider>
  </React.StrictMode>
);
