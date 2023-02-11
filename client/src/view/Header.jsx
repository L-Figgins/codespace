import React from "react";
import { Link } from "react-router-dom";
import avatarPlaceHolder from "../assets/avatar-placeholder.png";

function Header() {
  return (
    <>
      <div className="grid grid-cols-12 grid-rows-1 ">
        <img className="col-span-2 row-span-2" src={avatarPlaceHolder} />

        <div className="text-xl font-medium text-black  justify-self-start flex flex-col col-span-2">
          <div>Client Name</div>
          <div className="justify-self">Full Stack Software Engineer</div>
        </div>
        <div className="text-slate-500 row-start-1 col-start-5 col-span-6 row-span-2">
          A description of the client: Lorem ipsum dolor sit amet, consectetur
          adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore
          magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation
          ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute
          irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
          fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident,
          sunt in culpa qui officia deserunt mollit anim id est laborum.
        </div>
        <div className="col-span-1 justify-self-end col-start-11 col-span-2">
          <Link to={"signup"}>
            <button className="inline-flex justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">
              Signup
            </button>
          </Link>
          <Link to={"about"}>
            <button className="inline-flex justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">
              About
            </button>
          </Link>
          <Link to={"signin"}>
            <button className="inline-flex justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">
              Sign In
            </button>
          </Link>
          {/* </div> */}
        </div>
      </div>
    </>
  );
}

export default Header;
