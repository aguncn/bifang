import axios from 'axios'
import Cookie from 'js-cookie'

// 跨域认证信息 header 名
const authHeader = 'Authorization'

axios.defaults.timeout = 5000
axios.defaults.withCredentials= true

// http method
const METHOD = {
  GET: 'get',
  POST: 'post'
}

/**
 * axios请求
 * @param url 请求地址
 * @param method {METHOD} http method
 * @param params 请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
async function request(url, method, params) {
  switch (method) {
    case METHOD.GET:
      return axios.get(url, {params})
    case METHOD.POST:
      return axios.post(url, params)
    default:
      return axios.get(url, {params})
  }
}

//request拦截器
const reqInterceptor = {
    onFulfilled(config,$message){
        if (!Cookie.get(authHeader)) {
            $message.warning('认证 token 已过期，请重新登录')
        }
        return config
    },
    onRejected(error, $message) {
        $message.error(error.message)
        return Promise.reject(error)
    }
}
//respone拦截器
const resInterceptor = {
  onFulfilled(response, $message) {
    if (response.status === 401) {
        $message.error('无此接口权限')
    }
    return response
  },
  onRejected(error, $message) {
    $message.error(error.message)
    return Promise.reject(error)
  }
}
//初始化axios拦截器
function initInterceptor($message){
    axios.interceptors.request.use(
        config => reqInterceptor.onFulfilled(config, $message),
        error => reqInterceptor.onRejected(error, $message)
    )

    axios.interceptors.response.use(
        config => resInterceptor.onFulfilled(config, $message),
        error => resInterceptor.onRejected(error, $message)
    )
}



export {
    METHOD,
    request,
    initInterceptor
}