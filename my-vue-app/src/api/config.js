import axios from 'axios';

// 创建实例
const FrontendService = axios.create({
  baseURL: "http://10.200.136.105:8000/",
  headers: {
    'Content-Type': 'application/json;charset:UTF-8'
  },
  timeout: 100000,
});


// 请求拦截器，添加 JWT 令牌到请求头
FrontendService.interceptors.request.use(
  function (config) {
    // 成功处理函数
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  function (error) {
    // 错误处理函数
    return Promise.reject(error);
  }
);

// 响应拦截器，处理 JWT 过期情况
FrontendService.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const refresh_token = localStorage.getItem('refresh_token');
        if (refresh_token) {
          const response = await FrontendService.post('/api/token/refresh/', { refresh: refresh_token });
          const new_access_token = response.data.access;
          originalRequest.headers['Authorization'] = `Bearer ${new_access_token}`;
          localStorage.setItem('access_token', new_access_token);
          return FrontendService(originalRequest);
        }
      } catch (refreshError) {
        console.error(refreshError);
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        alert('您的登录已过期，请重新登录。');

        // 重定向到登录页面
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);
export default FrontendService;
