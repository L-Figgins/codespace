import "./App.css";
import Header from "./view/Header";
import SignUp from "./view/SignUp";
import AboutMe from "./view/AboutMe";
import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<Header />} />
        <Route path="signup" element={<SignUp />} />
        <Route path="about" element={<AboutMe />} />
      </Routes>
    </div>
  );
}

export default App;
