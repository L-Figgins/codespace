import { ExclamationCircleIcon } from "@heroicons/react/20/solid";
import { useFormControl } from "../FormControl";
import classNames from "../../utils/classnames";

export default function ValidatedInput({ id, name, ...props }) {
  const { required, error } = useFormControl();
  const errorClass = error
    ? "text-red-900 ring-1 ring-red-300 placeholder:text-red-300 focus:ring-red-500"
    : null;
  console.warn(error);
  return (
    <div className="relative mt-2 rounde\d-md shadow-sm">
      <input
        id={id}
        required={required}
        className={classNames(
          errorClass,
          "block w-full py-1.5 pr-10 ring-1 ring-inset focus:ring-2 focus:ring-inset border-0 rounded-md border-gray-300 shadow-sm sm:text-sm sm:leading-6"
        )}
        aria-invalid={String(Boolean(error))}
        aria-describeby={`${name}-error`}
        {...props}
      />
      {error && (
        <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-3">
          <ExclamationCircleIcon className="h-5 w-5 text-red-500" />
        </div>
      )}
    </div>
  );
}
