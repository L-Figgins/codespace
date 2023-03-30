import { useState, useEffect } from "react";
import { useFormData } from "./use-form-data";

/**
 * @callback ValidateFunction
 * @param {Object} - formData
 * @returns {Object}
 */

/**
 *
 * @param {Object} initialValue - intialFormState
 * @param {ValidateFunction} validate - validate function
 * @param {Function} submit - submit function
 * @returns {Object} - obj containing
 */
export function useFormValidation(initialValue, validate, onSubmit) {
  const { formData, handleChange, loadInitialData } = useFormData(initialValue);
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  console.log("FormData", JSON.stringify(formData, null, 4));

  useEffect(() => {
    if (isSubmitting) {
      const noErrors = Object.keys(errors).length === 0;
      if (noErrors) {
        onSubmit(formData);
      }
      setIsSubmitting(false);
    }
  }, [errors]);

  function handleSubmit(e) {
    e.preventDefault();
    const validationErrors = validate(formData);
    setErrors(validationErrors);
    setIsSubmitting(true);
  }

  function handleBlur(e) {
    console.log(e);
    const validationErrors = validate(formData);
    setErrors(validationErrors);
  }

  return {
    formData,
    handleChange,
    handleSubmit,
    handleBlur,
    loadInitialData,
    errors,
  };
}
