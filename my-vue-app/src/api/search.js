import request from './request'
import { handleError } from '../error/handleError';
const getRandomNumber = (numNo) => {
    return request.post({
        url:'/KnGraph/getRandom/',
        data:{"numNo":numNo},
    })
    .then(response => {
        console.log("getRandomNumber API响应数据：", response.data);
        return response.data;
    })
    .catch(error => {
        console.error("获取随机数错误:", error); // 处理可能的错误
        throw error;
    });
}

const getSearchForm = (form) => {
    return request.post({
        url:'/KnGraph/search_relation/',
        data:form,
    })
    .then(response => {
        console.log("getSearchForm API响应数据：", response.data);
        return response.data;
    })
    .catch(error => {
        console.error("获取图谱错误:", error); // 处理可能的错误
        handleError(error, "获取图谱搜索结果失败");
        throw error;
    });
}

const getAiAnswer = (question) => {
    return request.post({
        url:'/KnGraph/AI_answer/',
        data:{"question":question},
    })
    .then(response => {
        console.log("getAiAnswer API响应数据：", response.data);
        return response.data;
    })
    .catch(error => {
        console.error("获取AI问答结果错误:", error); // 处理可能的错误
        handleError(error, "获取AI问答结果失败");
        throw error;
    });
}

export default{getRandomNumber , getSearchForm , getAiAnswer};
