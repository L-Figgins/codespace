// Top level App component
import React, { createContext, useContext, useState } from "react";
import * as api from "../utils/api";

const authContext = createContext();
export function ProvideAuth({ children }) {
  const auth = useProvideAuth();
  return <authContext.Provider value={auth}>{children}</authContext.Provider>;
}

export const useAuth = () => {
  return useContext(authContext);
};

function useProvideAuth() {
  const [user, setUser] = useState(null);

  const login = (credentials) => {
    return api.login(credentials).then((user) => {
      setUser(user);
    });
  };

  const logout = () => {
    return api
      .logout()
      .then(() => {
        setUser(null);
      })
      .catch((err) => {
        console.error(err);
      });
  };

  return { user, login, logout };
}
