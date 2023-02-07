import React from "react";

function IndigoButton({ id, text, handleClick }, ref) {
  return (
    <button
      id={id}
      ref={ref}
      onClick={handleClick}
      className="p-5 inline-flex justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
    >
      {text}
    </button>
  );
}

const Forwarded = React.forwardRef(IndigoButton);
export default Forwarded;
