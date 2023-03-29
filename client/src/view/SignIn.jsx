import React, { useState } from "react";
import { useAuth } from "../hooks/use-auth";
import { useFormData } from "../hooks/use-form-data";
import { ValidationError } from "../shared/FormControl";
import AuthButton from "../components/AuthButton";

function SignIn() {
  const auth = useAuth();
  const [invalidCredentials, setInvalidCredentials] = useState(false);
  const { formData, handleChange } = useFormData({
    username: "",
    password: "",
  });

  const onSubmit = (e) => {
    e.preventDefault();
    e.stopPropagation();

    auth.login(formData).catch((err) => {
      if (err.response.status == 400) {
        setInvalidCredentials(true);
      }
    });
  };

  return (
    <div className="items-start justify-center mx-auto px-6 pt-10 pb-24 sm:pb-32 lg:flex lg:py-40 lg:px-8">
      {/* {form start} */}
      <div className="justify-center mx-auto mt-16 flex max-w-2xl sm:mt-24 lg:ml-0 lg:mt-0 lg:mr-0 lg:max-w-none lg:flex-none">
        <div className="flex min-h-full items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
          <div className="w-full max-w-md space-y-7">
            <div>
              <h2 className="mt-6 text-center text-3xl font-bold tracking-tight text-white">
                Sign in to your account
              </h2>
            </div>
            <form className="mt-8 space-y-6">
              <ValidationError
                visible={invalidCredentials}
                msg="Invalid Username or Password"
              />

              <input type="hidden" name="remember" defaultValue="true" />
              <div className="-space-y-px rounded-md shadow-sm">
                <div>
                  <label htmlFor="username" className="sr-only">
                    Username
                  </label>
                  <input
                    id="username"
                    name="username"
                    type="username"
                    required
                    value={formData.username}
                    onChange={handleChange}
                    className="relative block w-full appearance-none rounded-none rounded-t-md border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                    placeholder="Username"
                  />
                </div>
                <div>
                  <label htmlFor="password" className="sr-only">
                    Password
                  </label>
                  <input
                    id="password"
                    name="password"
                    type="password"
                    autoComplete="current-password"
                    required
                    onChange={handleChange}
                    className="relative block w-full appearance-none rounded-none rounded-b-md border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                    placeholder="Password"
                  />
                </div>
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <input
                    id="remember-me"
                    name="remember-me"
                    type="checkbox"
                    className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                  />
                  <label
                    htmlFor="remember-me"
                    className="ml-2 block text-sm text-gray-900"
                  >
                    Remember me
                  </label>
                </div>

                <div className="text-sm">
                  <a
                    href="#"
                    className="font-medium text-indigo-600 hover:text-indigo-500"
                  >
                    Forgot your password?
                  </a>
                </div>
              </div>

              <AuthButton onSubmit={onSubmit}>Sign In</AuthButton>
            </form>
          </div>
        </div>
      </div>
      {/* {form end} */}
    </div>
  );
}

export default SignIn;
