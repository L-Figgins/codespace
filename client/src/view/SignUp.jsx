import React, { useState } from "react";
import { useAuth } from "../hooks/use-auth";
import { useFormData } from "../hooks/use-form-data";
import AuthButton from "../components/AuthButton";
import Input from "../shared/Input";
import FormControl from "../shared/FormControl/";

const DEFAULT_LABEL_CLASSES =
  "block text-sm font-medium leading-6 text-gray-900";

export default function SignUp() {
  const { formData, handleChange } = useFormData({ email: "" });
  const auth = useAuth();

  const onSubmit = (e) => {
    e.preventDefault();
    e.stopPropagation();
    console.log(JSON.stringify(formData));
    auth.signup(formData);
  };

  return (
    <div className="items-start justify-center mx-auto px-6 pt-10 pb-24 sm:pb-32 lg:flex lg:py-20 lg:px-8">
      <div className="mt-10 sm:mt-0 flex justify-center">
        <div className="md:grid md:grid-cols-2 md:gap-6">
          <div className="mt-5 md:col-span-2 md:mt-0">
            <div>
              <h2 className="mt-6 mb-2 text-center text-3xl font-bold tracking-tight text-white">
                Create an Account
              </h2>
            </div>
            <form>
              <div className="overflow-hidden shadow sm:rounded-md">
                <div className="bg-white px-4 py-5 sm:p-6 rounded-md">
                  <div className="grid grid-cols-6 gap-6">
                    <div className="col-span-6 sm:col-span-3">
                      <FormControl onChange={handleChange} error="">
                        <label htmlFor="name" className={DEFAULT_LABEL_CLASSES}>
                          Name:
                        </label>
                        <Input
                          type="text"
                          name="name"
                          id="name"
                          autoComplete="given-name"
                          placeholder="John Smith"
                        />
                      </FormControl>
                    </div>
                    <div className="col-span-6 sm:col-span-3">
                      <FormControl
                        name="email"
                        onChange={handleChange}
                        error=""
                        // error={{ msg: "hello" }}
                      >
                        <label
                          htmlFor="email"
                          className={DEFAULT_LABEL_CLASSES}
                        >
                          Email:
                        </label>
                        <Input
                          value={formData.email}
                          type="text"
                          name="email"
                          placeholder="you@example.com"
                          id="email"
                          autoComplete="email"
                        />
                      </FormControl>
                    </div>

                    <div className="col-span-6 sm:col-span-3">
                      <FormControl
                        name="username"
                        onChange={handleChange}
                        error=""
                      >
                        <label
                          htmlFor="email"
                          className={DEFAULT_LABEL_CLASSES}
                        >
                          Username:
                        </label>
                        <Input
                          type="text"
                          name="username"
                          id="username"
                          autoComplete="username"
                          placeholder="username"
                        />
                      </FormControl>
                    </div>

                    <div className="col-span-6 sm:col-span-3">
                      <FormControl
                        name="password"
                        onChange={handleChange}
                        error=""
                      >
                        <label
                          htmlFor="email"
                          className={DEFAULT_LABEL_CLASSES}
                        >
                          Password
                        </label>

                        <Input
                          type="password"
                          name="password"
                          id="password"
                          autoComplete="new-password"
                        />
                      </FormControl>
                    </div>

                    <div className="col-span-6 sm:col-span-6 lg:col-span-2">
                      <FormControl
                        name="phone"
                        onChange={handleChange}
                        error=""
                      >
                        <label
                          htmlFor="phone"
                          className={DEFAULT_LABEL_CLASSES}
                        >
                          Phone:
                        </label>
                        <Input
                          type="text"
                          name="phone"
                          id="phone"
                          autoComplete="tel"
                        />
                      </FormControl>
                    </div>

                    <div className="col-span-6 sm:col-span-3 lg:col-span-2">
                      <FormControl
                        name="github"
                        onChange={handleChange}
                        error=""
                      >
                        <label
                          htmlFor="github"
                          className={DEFAULT_LABEL_CLASSES}
                        >
                          GitHub:
                        </label>
                        <Input
                          type="text"
                          name="github"
                          id="github"
                          autoComplete="url"
                        />
                      </FormControl>
                    </div>

                    <div className="col-span-6 sm:col-span-3 lg:col-span-2">
                      <FormControl
                        name="linked-in"
                        onChange={handleChange}
                        error=""
                      >
                        <label
                          htmlFor="linked-in"
                          className={DEFAULT_LABEL_CLASSES}
                        >
                          LinkedIn:
                        </label>
                        <Input
                          type="text"
                          name="linked-in"
                          id="linked-in"
                          autoComplete="url"
                        />
                      </FormControl>
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
