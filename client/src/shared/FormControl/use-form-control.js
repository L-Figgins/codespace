import { useContext } from "react";
import FormControlContext from "./form-control-context";
function useFormControl() {
  const context = useContext(FormControlContext);
  if (!context) {
    throw new Error(
      "useFormControl must be used within a FormControl component"
    );
  }
  return context;
}

export default useFormControl;
