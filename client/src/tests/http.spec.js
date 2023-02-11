import http from "../utils/http";

describe("axios http instance", () => {
  it("should have the correct base URL", () => {
    expect(http.defaults.baseURL).toBe("/api");
  });
});

describe("Interceptors", () => {
  //this inteceptor will be renamed in a future commit
  describe("responseHandler", () => {
    it("should unpack payload if present", () => {
      const res = {
        status: 200,
        data: {
          payload: {
            values: [1, 2, 3],
          },
        },
      };

      const unpackedRes = http.interceptors.response.handlers[0].fulfilled(res);
      expect(unpackedRes).toEqual({ values: [1, 2, 3] });
    });
  });

  describe("requestInt", () => {
    it("should format post data", () => {
      const config = {
        method: "post",
        url: "/testurl",
        data: [1, 2, 3],
      };
      const formatedConfig =
        http.interceptors.request.handlers[0].fulfilled(config);
      expect(formatedConfig).toMatchObject({
        method: "post",
        url: "/testurl",
        data: { payload: [1, 2, 3] },
      });
    });
  });
});
