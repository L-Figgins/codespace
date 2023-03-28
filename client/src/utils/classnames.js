/**
 * Small utility function for joining all truthy values into a class string
 * @param  {...any} classes
 * @returns
 */
export default function classNames(...classes) {
  return classes.filter(Boolean).join(" ");
}
