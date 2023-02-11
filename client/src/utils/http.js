import axios from "axios";
import {
  responseHandler,
  responseErrorHandler,
  requestErrorInt,
  requestInt,
} from "./inteceptors";

const http = axios.create({
  baseURL: "/api",
  timeout: 1000,
});

http.defaults.headers.post["Content-Type"] = "application/json";

// attach inteceptors to instance
http.interceptors.request.use(requestInt, requestErrorInt);
http.interceptors.response.use(responseHandler, responseErrorHandler);

export default http;
