import React from "react";

function LandingContent() {
  return (
    <div className="mx-auto px-6 pt-10 pb-24 sm:pb-32 lg:flex lg:py-40 lg:px-8">
      <div className="mx-auto max-w-2xl flex-shrink-0 lg:mx-0 lg:max-w-xl lg:pt-8">
        {/* <div className="mt-24 sm:mt-32 lg:mt-16">
            <a href="#" className="inline-flex space-x-6">
              <span className="rounded-full bg-indigo-500/10 px-3 py-1 text-sm font-semibold leading-6 text-indigo-400 ring-1 ring-inset ring-indigo-500/20">
                What's new
              </span>
              <span className="inline-flex items-center space-x-2 text-sm font-medium leading-6 text-gray-300">
                <span>Just shipped v1.0</span>
                <ChevronRightIcon
                  className="h-5 w-5 text-gray-500"
                  aria-hidden="true"
                />
              </span>
            </a>
          </div> */}
        <h1 className="mt-10 text-4xl font-bold tracking-tight text-white sm:text-6xl">
          Logan Figgins
        </h1>
        <p className="mt-6 text-lg leading-8 text-gray-300">
          Full Stack Software Engineer with a diverse set of skills and
          interests. Experienced working with scrum teams and project managers
          in a fast paced startup environment to deliver quality software
          deliverables and drive projects forward from concept to launch. A life
          long learner and firm believer in leaving code better than you found
          it.
        </p>
        <div className="mt-10 flex items-center gap-x-6">
          <a
            href="#"
            className="rounded-md bg-indigo-500 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-400"
          >
            Contact Me
          </a>
          <a href="#" className="text-sm font-semibold leading-6 text-white">
            Get My resume<span aria-hidden="true"> &#8595;</span>
          </a>
        </div>
      </div>

      <div className=" mx-auto mt-16 flex max-w-2xl sm:mt-24 lg:ml-10 lg:mt-0 lg:mr-0 lg:max-w-none lg:flex-none xl:ml-32">
        <div className="max-w-3xl flex-none sm:max-w-5xl lg:max-w-none">
          <img
            src="https://tailwindui.com/img/component-images/dark-project-app-screenshot.png"
            alt="App screenshot"
            // width={2432}
            // height={1442}
            className="w-[76rem] rounded-md bg-white/5 shadow-2xl ring-1 ring-white/10"
          />
        </div>
      </div>
    </div>
  );
}

export default LandingContent;
