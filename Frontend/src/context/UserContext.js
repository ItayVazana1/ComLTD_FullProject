import React, { createContext, useContext, useState } from 'react';

// Create UserContext
const UserContext = createContext();

// Provider Component
export const UserProvider = ({ children }) => {
  const [userData, setUserData] = useState(null);

  return (
    <UserContext.Provider value={{ userData, setUserData }}>
      {children}
    </UserContext.Provider>
  );
};

// Hook for consuming context
export const useUser = () => useContext(UserContext);
