import { useState } from "react";
import { camelCase, trim } from "lodash";

export function useFormData(intialValue) {
  const [formData, setFormData] = useState(intialValue);

  function handleChange(e) {
    setFormData((prevState) => {
      return { ...prevState, [camelCase(e.target.name)]: trim(e.target.value) };
    });
  }

  function loadInitalFormData(data) {
    setFormData(data);
  }

  const inputProps = {
    formData,
    onChange: handleChange,
    loadInitalFormData,
  };

  return inputProps;
}
