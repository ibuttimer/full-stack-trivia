import { useContext, createContext, useState } from "react";

export const AppContext = createContext({});

// https://levelup.gitconnected.com/how-to-use-context-with-react-hooks-5591a4010689
const ContextProvider = ({ children }) => {
    const [isAuthenticated, userHasAuthenticated] = useState(false);
    const [user, setUser] = useState(null);
    const context = {
        isAuthenticated, userHasAuthenticated,
        user, setUser
    };
    return (
        <AppContext.Provider value={ context }>
            {children}
        </AppContext.Provider>
    );
}

export default function useAppContext() {
  return useContext(AppContext);
}

export { ContextProvider, useAppContext };
