import classNames from "../../utils/classnames";
/**
 * Simple Error message component
 */
export default function ValidationError({ visible, children, id }) {
  return (
    <p
      id={`${id}-error`}
      className={classNames(
        visible ? "" : "invisible",
        "mt-2 text-sm text-red-600"
      )}
    >
      {/**  This is so it keeps the correct height, @TODO fix this with css */}
      {children}
    </p>
  );
}
