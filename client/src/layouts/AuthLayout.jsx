import React from "react";
import { Outlet } from "react-router-dom";

export default function AuthLayout() {
  return (
    <div className="items-start justify-center mx-auto px-6 pt-10 pb-24 sm:pb-32 lg:flex lg:py-40 lg:px-8">
      <div className="mt-10 sm:mt-0 flex justify-center">
        <div className="md:grid md:grid-cols-2 md:gap-6">
          <Outlet />
        </div>
      </div>
    </div>
  );
}
