import "./App.css";
import { BrowserRouter } from "react-router-dom";
import { NavBar } from "./components/NavBar";

function App() {
  return (
    <div className="bg-primary">
      <BrowserRouter>
        <NavBar />
      </BrowserRouter>
    </div>
  );
}

export default App;
