import { HttpError, NotImplementedError } from "../utils/errors";

describe("HttpError", () => {
  it("should have the correct name property", () => {
    const error = new HttpError("400 - error");
    expect(error.name).toBe("HttpError");
  });
  it("should have correct prototype", () => {
    const error = new HttpError("400 - error");
    expect(error instanceof Error).toBe(true);
    expect(error instanceof HttpError).toBe(true);
  });
});

describe("NotImplementedError", () => {
  it("should have the correct name property", () => {
    const error = new NotImplementedError();
    expect(error.name).toBe("NotImplementedError");
  });
  it("should have the correct default message", () => {
    const error = new NotImplementedError();
    expect(error.message).toBe("Not Implemented");
  });
  it("should have correct prototype", () => {
    const error = new NotImplementedError();
    expect(error instanceof Error).toBe(true);
    expect(error instanceof NotImplementedError).toBe(true);
  });
});
