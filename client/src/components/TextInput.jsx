import React from "react";
import { capitalize } from "lodash";

export default function TextInputField({
  id,
  title,
  placeholder = "",
  handleChange,
}) {
  return (
    <div className="flex justify-center">
      <div className="mb-3 xl:w-full">
        <label
          htmlFor={id}
          className="form-label inline-block mb-2 text-gray-700"
        >
          {capitalize(title)}
        </label>
        <input
          type="text"
          className="
        form-control
        block
        w-full
        px-3
        py-1.5
        text-base
        font-normal
        text-gray-700
        bg-white bg-clip-padding
        border border-solid border-gray-300
        rounded
        transition
        ease-in-out
        m-0
        focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none
      "
          name={title}
          id={id}
          placeholder={placeholder}
          onChange={handleChange}
        />
      </div>
    </div>
  );
}
