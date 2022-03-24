import { SupabaseClient } from "@supabase/supabase-js";
import { createContext, useContext, useState } from "react";

interface AppContextInterface {
  supabase: SupabaseClient;
  isSignedIn: boolean;
  setIsSignedIn: (isSignedIn: boolean) => void;
}

// @ts-ignore
const AppContext = createContext<AppContextInterface>({});

interface AppContextProviderProps {
  children: React.ReactNode;
}

const AppContextProvider = ({ children }: AppContextProviderProps) => {
  const supabase = new SupabaseClient(
    import.meta.env.VITE_SUPABASE_URL,
    import.meta.env.VITE_SUPABASE_ANON_KEY
  );
  const [isSignedIn, setIsSignedIn] = useState(false);
  supabase.auth.onAuthStateChange((event) => {
    if (event === "SIGNED_IN") {
      setIsSignedIn(true);
    } else if (event === "SIGNED_OUT" || event == "USER_DELETED") {
      setIsSignedIn(false);
    }
  });
  return (
    <AppContext.Provider value={{ supabase, isSignedIn, setIsSignedIn }}>
      {children}
    </AppContext.Provider>
  );
};

const useAppContext = () => useContext(AppContext);

export { AppContext, AppContextProvider, useAppContext };
