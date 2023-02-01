import axios from "axios";

/**
 * @typedef ContactInfo
 */

/**
 * @typedef ProfileInfo
 * @property {string} [description]
 * @property {string} [imageURL]
 * @property
 */

/**
 * @typedef User
 * @property {string} id - userID
 * @property {string} username - login username
 * @property {string} name - real name
 * @property {ProfileInfo}
 * @property {string} [password] - user password never returned only posted
 * @property {object} [contactInfo = {}] - optional contact conformation object
 * @property {string} [constactInfo.imageURL] - profile picture url
 * @property {string} [contactInfo.email] - user email addres
 * @property {string} [contactInfo.github] - github profile url
 * @property {string} [contactInfo.phone] - phone number
 * @property {string} [contactInfo.linkedIn] - linked in url
 */

/**
 * @typedef CodeSnippet
 * @property {string} code - code contents
 * @property {string} lang - code language
 */

/**
 * @typedef Article
 * @property {string} title - article title
 * @property {string} description - descript of code snippet post
 * @property {number} createdAt - timestamp of local date <-- changed
 * @property {CodeSnippet} code - snippet string
 *
 */

const ROUTES = {
  AUTH: "auth",
  ARTICLES: "articles",
};

function formatPostBody(data) {
  return {
    payload: { ...data },
  };
}

const API = {
  PREFIX: "api",

  /**
   * Route /<prefix>/user
   * Method GET admin user if they exist
   * @return {Promise<User | null>} Admin user or null if before configuration
   */
  async fetchAdminUser() {},

  /**
   * Route /<prefix>/auth/register
   * POST request to create admin user
   * @param {User} user - user info object
   * @return {Promise<object>} - success or payload
   */
  async createAdminUser(user) {
    const endpoint = `${API.PREFIX}/auth/register`;
    if (!user || !user.username || !user.password) {
      throw new TypeError("No Username or Password Provided. Invalid User.");
    }

    const transformData = (data) => {
      const CONTACT_INFO_KEYS = new Set([
        "email",
        "github",
        "linkedIn",
        "phone",
      ]);
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

    return axios.post(endpoint, formatPostBody(transformData(user)));
  },

  /**
   * Route /<prefix>/admin/image
   * Method POST
   */
  async uploadImage() {
    //pass
  },

  /**
   * route
   * METHOD: POST
   * @param {string} description - user description blurb
   * @return {Promise<object>} - response obj
   */
  async setProfileDescription() {},

  /**
   * METHOD: GET
   * Route /<prefix>/user/description
   * @param {string} description - user description blurb
   * @return {Promise<object>} - response obj
   */
  async fetchProfileDescription() {},

  // Auth prefix

  /**
   * Route auth/login
   * @param {object} obj - login object
   * @param {string} obj.username - account name
   * @param {string} obj.password - user password
   * @return {Promise<object>}
   */
  login({ username, password }) {
    //pass
  },

  logout() {
    //pass
  },
  /**
   *Get all articles
   * Route /<prefix>/articles?from= & limit
   * @return {Array<Article>} - returns aa
   */
  async getArticles() {
    //pass
    const endpoint = `${API.PREFIX}/${ROUTES.ARTICLES}`;
    return axios.get(endpoint).then((res) => {
      return res.data.payload;
    });
  },

  /**
   * Create a new article
   * Route /<prefix>/user/articles
   * Method POST create a new article
   * @param {Article} article - article object
   * @return {Promise<object>} - success or payload
   */

  async createArticle(article) {
    const endpoint = `${API.PREFIX}/${ROUTES.ARTICLES}`;
    if (typeof article !== object) {
      throw new TypeError(`Expected and object got ${typeof article}`);
    }
    return axios.post(endpoint, article);
  },

  /**
   * Route /<prefix>/articles/:id
   * Method GET get one article
   * @param {string} id - article's id
   * @return {Promise<Article>} - article object
   *
   * */
  async getArticle(id) {},
};

window.API = API;

export default API;
