import React, { useState } from "react";
import { useAuth } from "../../hooks/use-auth";
import { useFormData } from "../../hooks/use-form-data";
import { ValidationError } from "../../shared/FormControl";
import AuthButton from "../../shared/AuthButton";
import RememberMe from "./RememberMe";
import ForgotPassword from "./ForgotPassword";

function SignIn() {
  const auth = useAuth();
  const [invalidCredentials, setInvalidCredentials] = useState(false);
  const [isRememberMeChecked, setRememberMeChecked] = useState(true);
  const { formData, handleChange, handleSubmit, handleBlur, errors } =
    useFormData({
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

  const handleCheckedChange = (e) => {
    e.stopPropagation();
    setRememberMeChecked(!isRememberMeChecked);
  };

  return (
    <div className="md:col-span-2">
      <div className="w-full max-w-md space-y-7">
        <div>
          <h2 className="mt-6 text-center text-3xl font-bold tracking-tight text-white">
            Sign in to your account
          </h2>
        </div>
        <form className="mt-8 space-y-6">
          <ValidationError
            visible={invalidCredentials}
            id="login-validation-error"
          >
            Invalid Username or Password
          </ValidationError>

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
            <RememberMe
              isChecked={isRememberMeChecked}
              handleCheckedChange={handleCheckedChange}
              color="white"
            />

            <ForgotPassword />
          </div>
          <AuthButton onSubmit={onSubmit}>Sign In</AuthButton>
        </form>
      </div>
    </div>
  );
}

export default SignIn;
