import { ElMessage } from 'element-plus';
export const handleError = (error, defaultMessage = "系统错误") => {
    let errorMessage = defaultMessage;
    if (error.response) {
      const { data, status, statusText } = error.response;
      errorMessage = `状态码: ${status} (${statusText}), 错误信息: ${data.message || "未知错误"}`;
    } else if (error.request) {
      errorMessage = "网络错误：请求无法到达服务器！";
    } else {
      errorMessage = error.message;
    }
    ElMessage.error({
      message:errorMessage,
      duration: 5000,
      showClose:true
    }); // 弹出提示框
    throw new Error(errorMessage);
  };