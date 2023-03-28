import "./App.css";
import LandingContent from "./view/LandingContent";
import SignUp from "./view/SignUp";
import AboutMe from "./view/AboutMe";
import SignIn from "./view/SignIn";
import PublishArticle from "./view/PublishArticle";
import Profile from "./view/Profile";
import ArticleListElement from "./view/ArticleFeed";
import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Dashboard from "./view/Dashboard";
import { useAuth } from "./hooks/use-auth";
import { useEffect } from "react";
import * as api from "./utils/api";
import MainLayout from "./layouts/MainLayout";

function App() {
  //get userSesions
  const auth = useAuth();

  useEffect(() => {
    async function fetchData() {
      try {
        const user = await api.fetchUser();
        auth.setUser(user);
      } catch (e) {
        console.warn("user must authenticate");
      }
    }
    fetchData();
  }, []);

  return (
    <div className="App">
      <Navbar />
      <MainLayout>
        <Routes>
          <Route path="/" element={<LandingContent />} />
          <Route path="signup" element={<SignUp />} />
          <Route path="about" element={<AboutMe />} />
          <Route path="signin" element={<SignIn />} />
          <Route path="publish" element={<PublishArticle />} />
          <Route path="dashboard" element={<Dashboard />}>
            <Route index element={<Profile />} />
          </Route>
          <Route path="feed" element={<ArticleListElement />} />
        </Routes>
      </MainLayout>
    </div>
  );
}

export default App;
