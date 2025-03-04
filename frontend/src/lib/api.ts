import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

// interface ApiResponse<T> {
//     data: T;
//   }
  
export default api;