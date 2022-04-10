import "./App.css";
import { useNavigate, Routes, Route } from "react-router-dom";
import {
  MantineProvider,
  ColorSchemeProvider,
  ColorScheme,
} from "@mantine/core";
import { NotificationsProvider } from "@mantine/notifications";
import { SpotlightProvider } from "@mantine/spotlight";
import { Shell } from "./components/Shell";
import { lazy, useState } from "react";
import { Icon } from "./utils";
import { MDXProvider } from "@mdx-js/react";
import { ModalsProvider } from "@mantine/modals";

const NotFound = lazy(() => import("./pages/NotFound"));

const App = () => {
  const navigate = useNavigate();
  const localStorageColorScheme = localStorage.getItem("colorScheme");
  const [colorScheme, setColorScheme] = useState<ColorScheme>(
    localStorageColorScheme === "light" ? "light" : "dark"
  );
  const toggleColorScheme = (value?: ColorScheme) => {
    if (value === undefined) {
      value = colorScheme === "dark" ? "light" : "dark";
      setColorScheme(value);
    } else {
      setColorScheme(value);
    }
    localStorage.setItem("colorScheme", value);
  };
  return (
    <div className="App">
      <MDXProvider>
        <ColorSchemeProvider
          colorScheme={colorScheme}
          toggleColorScheme={toggleColorScheme}
        >
          <MantineProvider
            theme={{
              colorScheme,
              spacing: { xxs: 5, xxxs: 2 },
              primaryColor: "violet",
            }}
          >
            <NotificationsProvider>
              <ModalsProvider>
                <SpotlightProvider
                  shortcut={["mod + K", "mod + P", "/"]}
                  actions={[
                    {
                      title: "Home",
                      description: "Home page",
                      onTrigger: () => navigate("/"),
                      icon: <Icon.Home />,
                    },
                    {
                      title: "Docs",
                      description: "Documentation",
                      onTrigger: () => console.log("/docs"),
                      icon: <Icon.Book />,
                    },
                  ]}
                  searchIcon={<Icon.Search size={18} />}
                  searchPlaceholder="Search..."
                  nothingFoundMessage="Nothing found..."
                  highlightQuery
                  transition={{
                    in: { transform: "translateY(0)", opacity: 1 },
                    out: { transform: "translateY(-20px)", opacity: 0 },
                    transitionProperty: "transform, opacity",
                  }}
                >
                  <Shell>
                    <Routes>
                      <Route
                        path="*"
                        element={
                          <Suspense fallback={<Loader />}>
                            <NotFound />
                          </Suspense>
                        }
                      />
                    </Routes>
                  </Shell>
                </SpotlightProvider>
              </ModalsProvider>
            </NotificationsProvider>
          </MantineProvider>
        </ColorSchemeProvider>
      </MDXProvider>
    </div>
  );
};

export default App;
