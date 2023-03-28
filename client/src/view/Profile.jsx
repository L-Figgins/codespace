import { useAuth } from "../hooks/use-auth";
import { useFormData } from "../hooks/use-form-data";
import { CircleSpinner } from "../components/Spinner";
import { useEffect } from "react";

const user = {
  name: "Debbie Lewis",
  handle: "deblewis",
  email: "debbielewis@example.com",
  imageUrl:
    "https://images.unsplash.com/photo-1517365830460-955ce3ccd263?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=4&w=320&h=320&q=80",
};
export default function Profile() {
  const auth = useAuth();
  const { formData, handleChange, loadInitalFormData } = useFormData({
    about: "",
    firstName: "",
    lastName: "",
    linkedIn: "",
    github: "",
  });

  console.log(auth?.user);

  useEffect(() => {
    loadInitalFormData({
      about: auth?.user?.about || "",
      firstName: auth?.user?.name.split(" ")[0],
      lastName: auth?.user?.name.split(" ")[1] || "",
      linkedIn: auth?.user?.contactInfo?.linkedIn,
      github: auth?.user?.contactInfo?.github,
    });
  }, [auth.user]);
  console.log(JSON.stringify(formData, null, 4));

  // return !auth.user ? (
  //   <CircleSpinner />
  // ) : (
  //   <>
  return (
    <form
      className="divide-y divide-gray-200 lg:col-span-9"
      action="#"
      method="POST"
    >
      <div className="py-6 px-4 sm:p-6 lg:pb-8">
        <div>
          <h2 className="text-lg font-medium leading-6 text-gray-900">
            Profile
          </h2>
          <p className="mt-1 text-sm text-gray-500">
            This information will be displayed publicly so be careful what you
            share.
          </p>
        </div>

        <div className="mt-6 flex flex-col lg:flex-row">
          <div className="flex-grow space-y-6">
            <div>
              <label
                htmlFor="about"
                className="block text-sm font-medium leading-6 text-gray-900"
              >
                About
              </label>
              <div className="mt-2">
                <textarea
                  id="about"
                  name="about"
                  rows={6}
                  className="mt-1 block w-full rounded-md border-0 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-sky-500 sm:py-1.5 sm:text-sm sm:leading-6"
                  value={formData.about}
                  onChange={handleChange}
                />
              </div>
            </div>
          </div>

          <div className="mt-6 flex-grow lg:mt-0 lg:ml-6 lg:flex-shrink-0 lg:flex-grow-0">
            <p
              className="text-sm font-medium leading-6 text-gray-900"
              aria-hidden="true"
            >
              Photo
            </p>
            <div className="mt-2 lg:hidden">
              <div className="flex items-center">
                <div
                  className="inline-block h-12 w-12 flex-shrink-0 overflow-hidden rounded-full"
                  aria-hidden="true"
                >
                  <img
                    className="h-full w-full rounded-full"
                    src={user.imageUrl}
                    alt=""
                  />
                </div>
                <div className="relative ml-5">
                  <input
                    id="mobile-user-photo"
                    name="user-photo"
                    type="file"
                    className="peer absolute h-full w-full rounded-md opacity-0"
                  />
                  <label
                    htmlFor="mobile-user-photo"
                    className="pointer-events-none block rounded-md py-2 px-3 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 peer-hover:ring-gray-400 peer-focus:ring-2 peer-focus:ring-sky-500"
                  >
                    <span>Change</span>
                    <span className="sr-only"> user photo</span>
                  </label>
                </div>
              </div>
            </div>

            <div className="relative hidden overflow-hidden rounded-full lg:block">
              <img
                className="relative h-40 w-40 rounded-full"
                src={user.imageUrl}
                alt=""
              />
              <label
                htmlFor="desktop-user-photo"
                className="absolute inset-0 flex h-full w-full items-center justify-center bg-black bg-opacity-75 text-sm font-medium text-white opacity-0 focus-within:opacity-100 hover:opacity-100"
              >
                <span>Change</span>
                <span className="sr-only"> user photo</span>
                <input
                  type="file"
                  id="desktop-user-photo"
                  name="user-photo"
                  className="absolute inset-0 h-full w-full cursor-pointer rounded-md border-gray-300 opacity-0"
                />
              </label>
            </div>
          </div>
        </div>

        <div className="mt-6 grid grid-cols-12 gap-6">
          <div className="col-span-12 sm:col-span-6">
            <label
              htmlFor="first-name"
              className="block text-sm font-medium leading-6 text-gray-900"
            >
              First name
            </label>
            <input
              type="text"
              name="first-name"
              id="first-name"
              onChange={handleChange}
              autoComplete="given-name"
              className="mt-2 block w-full rounded-md border-0 px-3 py-1.5 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:border-0 focus:ring-2 focus:ring-inset focus:ring-sky-500 sm:text-sm sm:leading-6"
              value={formData.firstName}
            />
          </div>

          <div className="col-span-12 sm:col-span-6">
            <label
              htmlFor="last-name"
              className="block text-sm font-medium leading-6 text-gray-900"
            >
              Last name
            </label>
            <input
              type="text"
              name="last-name"
              id="last-name"
              autoComplete="family-name"
              onChange={handleChange}
              value={formData.lastName}
              className="mt-2 block w-full rounded-md border-0 px-3 py-1.5 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:border-0 focus:ring-2 focus:ring-inset focus:ring-sky-500 sm:text-sm sm:leading-6"
            />
          </div>

          <div className="col-span-12 sm:col-span-6">
            <label
              htmlFor="linked-in"
              className="block text-sm font-medium leading-6 text-gray-900"
            >
              LinkedIn
            </label>
            <input
              value={formData.linkedIn}
              type="text"
              name="linked-in"
              onChange={handleChange}
              id="linked-in"
              className="mt-2 block w-full rounded-md border-0 px-3 py-1.5 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:border-0 focus:ring-2 focus:ring-inset focus:ring-sky-500 sm:text-sm sm:leading-6"
            />
          </div>

          <div className="col-span-12 sm:col-span-6">
            <label
              htmlFor="github"
              className="block text-sm font-medium leading-6 text-gray-900"
            >
              Github
            </label>
            <input
              type="text"
              name="github"
              id="github"
              value={formData.github}
              onChange={handleChange}
              className="mt-2 block w-full rounded-md border-0 px-3 py-1.5 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:border-0 focus:ring-2 focus:ring-inset focus:ring-sky-500 sm:text-sm sm:leading-6"
            />
          </div>
        </div>
      </div>

      <div className="divide-y divide-gray-200 pt-6">
        <div className="mt-4 flex justify-end gap-x-3 py-4 px-4 sm:px-6">
          <button
            type="button"
            className="inline-flex justify-center rounded-md bg-white py-2 px-3 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
          >
            Cancel
          </button>
          <button
            type="submit"
            className="inline-flex justify-center rounded-md bg-sky-700 py-2 px-3 text-sm font-semibold text-white shadow-sm hover:bg-sky-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-700"
          >
            Save
          </button>
        </div>
      </div>
    </form>
  );
  //   </>
  // );
}
