import clsx from "clsx";

export default function NumberInput({ label, error, ...props }) {
  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-1">{label}</label>
      <input
        type="number"
        {...props}
        className={clsx(
          "w-28 px-3 py-2 border rounded-md text-sm shadow-sm focus:ring-2 focus:ring-blue-500/40 focus:border-blue-500",
          error ? "border-red-400 ring-red-300" : "border-gray-200"
        )}
      />
      {error && <p className="mt-1 text-sm text-red-600">{error}</p>}
    </div>
  );
}
