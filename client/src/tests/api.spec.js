import axios from "axios";
import API from "../api/api";
import { beforeAll, beforeEach, describe, expect, it, vi } from "vitest";

describe("API tests", () => {
  beforeAll(() => {
    axios.post = vi.fn();
    axios.get = vi.fn();
  });
  beforeEach(() => {
    vi.resetAllMocks();
  });
  describe("createAdminUser", () => {
    it("should resolve if user is provided", async () => {
      const user = {
        username: "user",
        password: "pw123",
      };
      const expectedEndPoint = `${API.PREFIX}/auth/register`;
      axios.post.mockResolvedValue({
        status: 200,
        data: { payload: "Post successful" },
      });
      const response = await API.createAdminUser(user);
      expect(response.data).toEqual({ payload: "Post successful" });
      expect(axios.post).toHaveBeenCalledWith(expectedEndPoint, user);
    });
  });
  describe("getArticles", () => {
    it("should return an array of articles", async () => {
      const expectedEndPoint = `${API.PREFIX}/articles`;
      const expected = [
        { id: 1, data: {} },
        { id: 2, data: {} },
      ];
      const axiosRes = { data: { payload: expected }, status: 200 };
      axios.get.mockResolvedValue(axiosRes);
      const articles = await API.getArticles();
      expect(axios.get).toHaveBeenCalledWith(expectedEndPoint);
      expect(articles).toEqual(expected);
    });
  });
  describe("createArticle", () => {
    it("should succeed if article is provided");
  });
});
