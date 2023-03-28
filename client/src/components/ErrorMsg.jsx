import classNames from "../utils/classnames";
/**
 * Simple Error message component
 */
export default function ErrorMessage({ visible, msg }) {
  return (
    <div
      className={classNames(
        visible ? "" : "invisible",
        "font-bold text-red-800 w-full text-center"
      )}
    >
      {msg}
    </div>
  );
}
