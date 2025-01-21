import React, { createContext, useContext, useState } from 'react';

// Create UserContext
// This context will hold user-related data and allow components to access and update it.
const UserContext = createContext();

/**
 * UserProvider Component:
 * Wraps the application or part of it to provide access to user data and functions for updating it.
 * @param {Object} children - React components that require access to the UserContext.
 */
export const UserProvider = ({ children }) => {
  // State to store user data
  const [userData, setUserData] = useState(null);

  return (
    <UserContext.Provider value={{ userData, setUserData }}>
      {children} {/* Render child components inside the provider */}
    </UserContext.Provider>
  );
};

/**
 * useUser Hook:
 * A custom hook to consume the UserContext.
 * Allows easy access to `userData` and `setUserData` from any component.
 * @returns {Object} - An object containing `userData` and `setUserData`.
 */
export const useUser = () => useContext(UserContext);
