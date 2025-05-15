import request from './request'
import { handleError } from '../error/handleError';

const getCurrentUserId = ()=>{
  const token = localStorage.getItem('access_token');
  console.log("tokens：",token);
  if (!token) {
    console.warn("未找到JWT token");
    return null;
  }

  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    return payload.user_id || payload.sub; // sub 是标准JWT字段
  } catch (e) {
    console.error("获取用户ID失败", e);
    return null;
  }
};

const getUserPreferences = (user_id) => {
  return request.post({
      url:'/User/api/user_preferences/',
      data:{"user_id":user_id}
  })
  .then(response => {
      console.log("getUserPreferences API响应数据：", response.data);
      return response.data;
  })
  .catch(error => {
      console.error("获取user_id对应的偏好错误:", error); // 处理可能的错误
      handleError(error, "获取user_id对应的偏好失败");
      throw error;
  });
}

const alterUserPreferences = (user_id,preferences) => {
  return request.post({
      url:'/User/api/alterUserPreferences/',
      data:{"user_id":user_id,"preferences":preferences}
  })
  .then(response => {
      console.log("alterUserPreferences API响应数据：", response.data);
      return response.data;
  })
  .catch(error => {
      console.error("修改user_id对应的偏好错误:", error); // 处理可能的错误
      handleError(error, "修改user_id对应的偏好失败");
      throw error;
  });
}

const getUserRecommend = (user_id) => {
  return request.post({
      url:'/KnGraph/recommend/',//*/*/*/*/
      data:{"user_id":user_id}
  })
  .then(response => {
      console.log("getUserRecommend API响应数据：", response.data);
      return response.data;
  })
  .catch(error => {
      console.error("获得user_id对应的推荐错误:", error); // 处理可能的错误
      handleError(error, "获得user_id对应的推荐失败");
      throw error;
  });
}

  export default{getUserPreferences , alterUserPreferences , getCurrentUserId , getUserRecommend};