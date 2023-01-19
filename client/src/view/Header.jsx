import React from "react";
import avatarPlaceHolder from "../assets/avatar-placeholder.png";
function Header() {
  return (
    <div className="grid grid-cols-12 grid-rows-2 ">
      <img className="col-span-2 row-span-2" src={avatarPlaceHolder} />

      <div className="text-xl font-medium text-black  justify-self-start flex flex-col col-span-2">
        <div>Client Name</div>
        <div className="justify-self">Full Stack Software Engineer</div>
      </div>
      <div className="text-slate-500 row-start-1 col-start-5 col-span-6 row-span-2">
        A description of the client: Lorem ipsum dolor sit amet, consectetur
        adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore
        magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
        laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor
        in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
        pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa
        qui officia deserunt mollit anim id est laborum.
      </div>
      <div className="col-span-1 justify-self-end col-start-11 col-span-2">
        Socials or maybe a darkmode toggle button
      </div>
    </div>
  );
}

export default Header;
