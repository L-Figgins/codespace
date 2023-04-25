import { useState } from "react";
import { camelCase, trim } from "lodash";

export function useFormData(intialValue) {
  const [formData, setFormData] = useState(intialValue);

  function handleChange(e) {
    setFormData((prevState) => {
      console.log(e);
      return { ...prevState, [camelCase(e.target.name)]: trim(e.target.value) };
    });
  }

  function loadInitalFormData(data) {
    setFormData(data);
  }

  const inputProps = {
    formData,
    handleChange,
    loadInitalFormData,
  };

  return inputProps;
}
