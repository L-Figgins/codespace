import http from "./http";
import { NotImplementedError } from "./errors";

/**
 * @typedef ContactInfo
 * @property {string} [imageURL] - profile picture url
 */

/**
 * @typedef ProfileInfo
 * @property {string} [description]
 * @property {string} [imageURL]
 * @property {string} [github] - github profile url
 * @property {string} [phone] - phone number
 * @property {string} [linkedIn] - linked in url
 */

/**
 * @typedef User
 * @property {string} id - userID
 * @property {string} username - login username
 * @property {string} name - real name
 * @property {ProfileInfo}
 * @property {string} [password] - user password never returned only posted
 * @property {ContactInfo} [contactInfo] - optional contact conformation object
 */

/**
 * @typedef Article
 * @property {string} title - article title
 * @property {string} description - descript of code snippet post
 * @property {number} createdAt - timestamp of local date <-- changed
 * @property {String} markdown - blog markdown to be rendered into html
 *
 */

const ROUTES = {
  AUTH: "auth",
  ARTICLES: "articles",
};

/**
 * Route /<prefix>/user
 * Method GET admin user if they exist
 * @return {Promise<User | null>} Admin user or null if before configuration
 */
export const fetchUser = async () => {
  return http.get("/user");
};

/**
 * Route /<prefix>/auth/register
 * POST request to create admin user
 * @param {User} user - user info object
 * @return {Promise<object>} - success or payload
 */
export const createAdminUser = async (user) => {
  const endpoint = `/auth/register`;
  if (!user || !user.username || !user.password) {
    throw new TypeError("No Username or Password Provided. Invalid User.");
  }

  const transformData = (data) => {
    const CONTACT_INFO_KEYS = new Set(["email", "github", "linkedIn", "phone"]);
    const result = {
      contactInfo: {},
    };
    for (let key of Object.keys(data)) {
      if (CONTACT_INFO_KEYS.has(key)) {
        result.contactInfo[key] = data[key];
        continue;
      }
      result[key] = data[key];
    }
    return result;
  };

  return http.post(endpoint, transformData(user));
};

/**
 * Route auth/login
 * @param {object} obj - login object
 * @param {string} obj.username - account name
 * @param {string} obj.password - user password
 * @return {Promise<object>}
 */
export const login = (credentials) => {
  if (!credentials || !credentials.username || !credentials.password) {
    throw new TypeError("Missing User Credentials", {
      cause: { values: [credentials] },
    });
  }
  return http.post("/auth/login", credentials);
};

export const logout = () => {
  return http.get("/auth/logout");
};

/**
 * Create a new article
 * Route /<prefix>/user/articles
 * Method POST create a new article
 * @param {Article} article - article object
 * @return {Promise<object>} - success or payload
 */
export const createArticle = async (article) => {
  const endpoint = `/${ROUTES.ARTICLES}`;
  if (typeof article !== "object") {
    throw new TypeError(`Expects type object got ${typeof article}`, {
      cause: values[article],
    });
  }
  return http.post(endpoint, article);
};

/**
 * Get all articles
 * Route /<prefix>/articles?from= & limit
 * @return {Array<Article>} - returns aa
 */
export const getArticles = async () => {
  const endpoint = `/${ROUTES.ARTICLES}`;
  return http.get(endpoint);
};

/**
 * Upload image
 */
export const uploadImage = async () => {
  throw new NotImplementedError();
};
