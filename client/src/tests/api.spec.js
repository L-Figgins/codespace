import http from "../utils/http";
import * as API from "../utils/api";
import { beforeAll, beforeEach, describe, expect, it, vi } from "vitest";

describe("API tests", () => {
  beforeAll(() => {
    http.post = vi.fn();
    http.get = vi.fn();
  });
  beforeEach(() => {
    vi.resetAllMocks();
  });
  describe("createAdminUser", () => {
    it("should resolve if user is provided", async () => {
      const user = {
        username: "user",
        password: "pw123",
        email: "test@gmail.com",
        phone: "15555555",
      };
      const expectedEndPoint = `/auth/register`;
      http.post.mockResolvedValue({
        status: 200,
        data: { payload: "Post successful" },
      });
      const response = await API.createAdminUser(user);
      expect(response.data).toEqual({ payload: "Post successful" });
      expect(http.post).toHaveBeenCalledWith(expectedEndPoint, {
        username: "user",
        password: "pw123",
        contactInfo: {
          email: "test@gmail.com",
          phone: "15555555",
        },
      });
    });
  });
  describe("getArticles", () => {
    it("should return an array of articles", async () => {
      const expectedEndPoint = `/articles`;
      const expected = [
        { id: 1, data: {} },
        { id: 2, data: {} },
      ];
      // const httpRes = { data: { payload: expected }, status: 200 };
      //payload  unpacking is tested in the inteceptors spec
      http.get.mockResolvedValue(expected);
      const articles = await API.getArticles();
      expect(http.get).toHaveBeenCalledWith(expectedEndPoint);
      expect(articles).toEqual(expected);
    });
  });
  describe("createArticle", () => {
    it("should succeed if article is provided", () => {
      //pass
    });
  });
});
