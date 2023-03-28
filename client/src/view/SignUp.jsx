import React, { useState } from "react";
import { camelCase, trim } from "lodash";
import * as api from "../utils/api";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/use-auth";
import { useFormData } from "../hooks/use-form-data";
import AuthButton from "../components/AuthButton";

export default function SignUp() {
  const { formData, handleChange } = useFormData();
  const auth = useAuth();

  const onSubmit = (e) => {
    e.preventDefault();
    e.stopPropagation();
    console.log(JSON.stringify(formData));
    auth.signup(formData);
  };

  return (
    <div className="items-start justify-center mx-auto px-6 pt-10 pb-24 sm:pb-32 lg:flex lg:py-40 lg:px-8">
      <div className="mt-10 sm:mt-0 flex justify-center">
        <div className="md:grid md:grid-cols-2 md:gap-6">
          <div className="mt-5 md:col-span-2 md:mt-0">
            <div>
              <h2 className="mt-6 mb-2 text-center text-3xl font-bold tracking-tight text-white">
                Create an account
              </h2>
            </div>
            <form>
              <div className="overflow-hidden shadow sm:rounded-md">
                <div className="bg-white px-4 py-5 sm:p-6 rounded-md">
                  <div className="grid grid-cols-6 gap-6">
                    <div className="col-span-6 sm:col-span-3">
                      <label
                        htmlFor="name"
                        className="block text-sm font-medium text-gray-700"
                      >
                        Name
                      </label>
                      <input
                        type="text"
                        name="name"
                        id="name"
                        autoComplete="given-name"
                        onChange={handleChange}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                      />
                    </div>

                    <div className="col-span-6 sm:col-span-3">
                      <label
                        htmlFor="email"
                        className="block text-sm font-medium text-gray-700"
                      >
                        Email address
                      </label>
                      <input
                        type="text"
                        name="email"
                        id="email"
                        autoComplete="email"
                        onChange={handleChange}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                      />
                    </div>

                    <div className="col-span-6">
                      <label
                        htmlFor="username"
                        className="block text-sm font-medium text-gray-700"
                      >
                        Username
                      </label>
                      <input
                        type="text"
                        name="username"
                        id="username"
                        autoComplete="username"
                        onChange={handleChange}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                      />
                    </div>
                    <div className="col-span-6">
                      <label
                        htmlFor="password"
                        className="block text-sm font-medium text-gray-700"
                      >
                        Password
                      </label>
                      <input
                        type="text"
                        name="password"
                        id="password"
                        autoComplete="new-password"
                        onChange={handleChange}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                      />
                    </div>

                    <div className="col-span-6 sm:col-span-6 lg:col-span-2">
                      <label
                        htmlFor="phone"
                        className="block text-sm font-medium text-gray-700"
                      >
                        Phone
                      </label>
                      <input
                        type="text"
                        name="phone"
                        id="phone"
                        autoComplete="tel"
                        onChange={handleChange}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                      />
                    </div>

                    <div className="col-span-6 sm:col-span-3 lg:col-span-2">
                      <label
                        htmlFor="github"
                        className="block text-sm font-medium text-gray-700"
                      >
                        GitHub
                      </label>
                      <input
                        type="text"
                        name="github"
                        id="github"
                        autoComplete="url"
                        onChange={handleChange}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                      />
                    </div>

                    <div className="col-span-6 sm:col-span-3 lg:col-span-2">
                      <label
                        htmlFor="linkedIn"
                        className="block text-sm font-medium text-gray-700"
                      >
                        LinkedIn
                      </label>
                      <input
                        type="text"
                        name="linkedIn"
                        id="linkedIn"
                        autoComplete="url"
                        onChange={handleChange}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                      />
                    </div>
                  </div>
                </div>
                <div className="mt-2">
                  <AuthButton onSubmit={onSubmit}>Sign Up</AuthButton>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
