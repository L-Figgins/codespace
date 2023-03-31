import React, { useCallback } from "react";
import { useAuth } from "../../hooks/use-auth";
import { useFormValidation } from "../../hooks/use-form-validation";
import AuthButton from "../../components/AuthButton";
import Input from "../../shared/Input";
import FormControl from "../../shared/FormControl";
import validate from "./validate";

const DEFAULT_LABEL_CLASSES =
  "block text-sm font-medium leading-6 text-gray-900";

export default function SignUp() {
  const submitFunction = (data) => {
    auth.signup(data);
  };

  const { formData, handleChange, handleSubmit, handleBlur, errors } =
    useFormValidation(
      {
        name: "",
        password: "",
        github: "",
        username: "",
        email: "",
        phone: "",
        linkedIn: "",
      },
      validate,
      submitFunction
    );
  const auth = useAuth();
  return (
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
                <FormControl
                  onBlur={handleBlur}
                  onChange={handleChange}
                  error={errors.name}
                >
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
                  error={errors.email}
                  // error={{ msg: "hello" }}
                >
                  <label htmlFor="email" className={DEFAULT_LABEL_CLASSES}>
                    Email:
                  </label>
                  <Input
                    value={formData.email}
                    type="text"
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
                  error={errors.username}
                >
                  <label htmlFor="username" className={DEFAULT_LABEL_CLASSES}>
                    Username:
                  </label>
                  <Input
                    type="text"
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
                  error={errors.password}
                >
                  <label htmlFor="password" className={DEFAULT_LABEL_CLASSES}>
                    Password
                  </label>

                  <Input
                    type="password"
                    id="password"
                    autoComplete="new-password"
                  />
                </FormControl>
              </div>

              <div className="col-span-6 sm:col-span-6 lg:col-span-2">
                <FormControl
                  name="phone"
                  onChange={handleChange}
                  error={errors.phone}
                >
                  <label htmlFor="phone" className={DEFAULT_LABEL_CLASSES}>
                    Phone:
                  </label>
                  <Input type="text" id="phone" autoComplete="tel" />
                </FormControl>
              </div>

              <div className="col-span-6 sm:col-span-3 lg:col-span-2">
                <FormControl
                  name="github"
                  onChange={handleChange}
                  error={errors.github}
                >
                  <label htmlFor="github" className={DEFAULT_LABEL_CLASSES}>
                    GitHub:
                  </label>
                  <Input type="text" id="github" autoComplete="url" />
                </FormControl>
              </div>

              <div className="col-span-6 sm:col-span-3 lg:col-span-2">
                <FormControl
                  name="linked-in"
                  onChange={handleChange}
                  error={errors.linkedIn}
                >
                  <label htmlFor="linked-in" className={DEFAULT_LABEL_CLASSES}>
                    LinkedIn:
                  </label>
                  <Input type="text" id="linked-in" autoComplete="url" />
                </FormControl>
              </div>
            </div>
          </div>
          <div className="mt-2">
            <AuthButton onSubmit={handleSubmit}>Sign Up</AuthButton>
          </div>
        </div>
      </form>
    </div>
  );
}
