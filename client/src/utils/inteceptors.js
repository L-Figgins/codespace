/**
 * Formats post body to convention/
 * @param {Object} data - data to format
 * @returns
 */
function formatPostBody(data) {
  return {
    payload: { ...data },
  };
}

/**
 * Reponse inteceptor
 * @param {Axios} res - Axios Response
 * @returns
 */
export const responseHandler = (res) => {
  if (res?.payload) {
    return res.payload;
  }
  return res;
};

/**
 * Response Error Inteceptor
 * @param {Object} error - Error Object
 * @returns {Promise} - Promise.reject(error)
 */
export const responseErrorHandler = (error) => {
  console.error(error.toJSON());
  return Promise.reject(error);
};

/**
 * Request Inteceptor
 * @param {Object} config - Axios Request Config
 * @returns {Object}
 */
export const requestInt = (config) => {
  if (config.method === "post") {
    config.data = formatPostBody(config);
    return config;
  }
  return config;
};

/**
 * Request Error Inteceptor
 * @param {Object} Error - AxiosError Object
 */

export const requestErrorInt = (error) => {
  console.error(error);
  return Promise.reject(error);
};
