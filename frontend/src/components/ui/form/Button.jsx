import React from "react";

export default function Button({
  children,
  onClick,
  variant = "primary",
  disabled = false,
  className = "",
  ...props
}) {
  const baseClasses =
    "font-medium rounded-lg cursor-pointer transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2";

  const variants = {
    primary: "bg-primary hover:bg-primary-dark text-white focus:ring-primary",
    secondary:
      "bg-secondary hover:bg-secondary-dark text-white focus:ring-secondary",
    danger: "bg-danger hover:bg-danger-dark text-white focus:ring-danger",
    success: "bg-success hover:bg-success-dark text-white focus:ring-success",
  };

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`${baseClasses} ${variants[variant]} py-3 px-6 text-lg ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}
