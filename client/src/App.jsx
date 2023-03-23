import "./App.css";
import Home from "./view/Home";
import SignUp from "./view/SignUp";
import AboutMe from "./view/AboutMe";
import SignIn from "./view/SignIn";
import PublishArticle from "./view/PublishArticle";
import ArticleListElement from "./view/ArticleFeed";
import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import { ProvideAuth } from "./hooks/use-auth";

function App() {
  return (
    <ProvideAuth>
      <div className="App">
        <Navbar />
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="signup" element={<SignUp />} />
            <Route path="about" element={<AboutMe />} />
            <Route path="signin" element={<SignIn />} />
            <Route path="publish" element={<PublishArticle />} />
            <Route path="feed" element={<ArticleListElement />} />
          </Routes>
        </main>
      </div>
    </ProvideAuth>
  );
}

export default App;
