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
export function useFromValidation(initialValue, validate, submit) {
  const { formData, handleChange, loadInitialData } = useFormData({});
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (isSubmitting) {
      const noErrors = Object.keys(errors).length === 0;
      if (noErrors) {
        onSubmit(form);
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

  function handleBlur() {
    const validationErrors = validate(form);
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
