import LockSvg from "./LockSvg";

export default function AuthButton({ onSubmit, children }) {
  return (
    <button
      onClick={onSubmit}
      className="group relative flex w-full justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
    >
      <span className="absolute inset-y-0 left-0 flex items-center pl-3">
        <LockSvg />
      </span>
      {children}
    </button>
  );
}
