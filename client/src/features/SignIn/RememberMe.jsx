export default function RememberMe({ isChecked, handleCheckedChange, color }) {
  return (
    <div className="flex items-center">
      <input
        id="remember-me"
        name="remember-me"
        type="checkbox"
        checked={isChecked}
        className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
        onChange={handleCheckedChange}
      />
      <label
        htmlFor="remember-me"
        className={`ml-2 block text-sm text-${color}`}
      >
        Remember me
      </label>
    </div>
  );
}
