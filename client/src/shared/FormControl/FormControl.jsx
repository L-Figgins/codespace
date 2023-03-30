import React from "react";
import ValidationError from "./ValidationError";
import FormControlContext from "./form-control-context";

export default function FormControl({
  children,
  onChange,
  onBlur,
  error,
  name,
  ...props
}) {
  const contextValue = {
    name,
    onChange,
    error,
    ...props,
  };

  return (
    <FormControlContext.Provider value={contextValue}>
      {children}
      <ValidationError id={name} visible={Boolean(error)}>
        {error?.msg || "hidden"}
      </ValidationError>
    </FormControlContext.Provider>
  );
}
