import FrontendService from './config'

//封装get请求
const get = (config) => {
    return FrontendService({
        ...config,
        method:'get',
        params:config.data
    })
}

//封装post请求
const post = (config) => {
    return FrontendService({
        ...config,
        method:'post',
        data:config.data
    })
}

// 封装delete请求
const remove = (config) => {
    return FrontendService({
        ...config,
        method:'delete',
        params:config.data
    })
}

// 封装put请求
const put = (config) => {
    return FrontendService({
        ...config,
        method:'put',
        data:config.data
    })
}

export default{
    get,
    post,
    remove,
    put
};
