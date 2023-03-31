import isEmail from "validator/es/lib/isEmail";
import isPhoneNumber from "validator/es/lib/isMobilePhone";
import isAlphaNumeric from "validator/es/lib/isAlphanumeric";
import isUrl from "validator/es/lib/isURL";

export default function validate(data) {
  const errors = {};

  const validEmail = isEmail(data.email);
  if (!validEmail) {
    errors.email = { msg: "Invalid Email Address" };
  }

  const validPhone = isPhoneNumber(data.phone);
  if (!validPhone) {
    errors.phone = { msg: "Invalid Phone Number" };
  }

  const socialMediaFields = ["linkedIn", "github"];
  for (const social of socialMediaFields) {
    const valid = isUrl(data[social]);
    if (!valid) {
      errors[social] = { msg: `Invalid URL (${social})` };
    }
  }

  const validPassword = data.password.length > 3;
  if (!validPassword) {
    errors.password = { msg: "Invalid Password" };
  }

  const alphaNumericFields = ["username", "name"];
  for (const field of alphaNumericFields) {
    const valid = isAlphaNumeric(data[field]);
    if (!valid) {
      errors[field] = { msg: `${field}'s must be Alphanumeric` };
    }
  }

  console.log(JSON.stringify(errors, null, 4));
  /**@TODO ensure this works languages other than english, however there is no current requirement */
  return errors;
}
