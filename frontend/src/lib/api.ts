import axios from "axios";

const api = axios.create({
  baseURL: "http://192.168.0.159:8000",
});

// interface ApiResponse<T> {
//     data: T;
//   }
  
export default api;