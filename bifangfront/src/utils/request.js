import axios from 'axios'
import Cookie from 'js-cookie'

// 跨域认证信息 header 名
const authHeader = 'Authorization'

axios.defaults.timeout = 5000
axios.defaults.withCredentials= true

// http method
const METHOD = {
  GET: 'get',
  POST: 'post',
  DELETE: 'delete',
  PUT: 'put',
  PATCH: 'patch'
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
    case METHOD.DELETE:
      return axios.delete(url, params)
    case METHOD.PUT:
      return axios.put(url, params)
    case METHOD.PATCH:
        return axios.patch(url, params)
    default:
      return axios.get(url, {params})
  }
}

const whiteRequstList = [];
/**
 * 请求白名单
 * @param {*} apiList 
 */
function requestWhitelistConfig(apiList){
  Object.prototype.toString.call(apiList) === '[object Array]'?
  whiteRequstList.push.apply(whiteRequstList,apiList):whiteRequstList.push(apiList)
}

//request拦截器
const reqInterceptor = {
    onFulfilled(config,$message,router){
        const {url} = config;
        let token = Cookie.get(authHeader)
        config.headers.common[authHeader] = token
        config.headers['Content-Type'] = 'application/json';
        if (whiteRequstList.indexOf(url) === -1 && !Cookie.get(authHeader)) {
            $message.warning('认证 token 已过期，请重新登录');
            setTimeout(()=>{
              router.push('/login')
            },1000)
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
/**
 * 初始化axios拦截器
 * @param {*} $message 
 */
function initInterceptor($message,router){
    axios.interceptors.request.use(
        config => reqInterceptor.onFulfilled(config, $message,router),
        error => reqInterceptor.onRejected(error, $message)
    )

    axios.interceptors.response.use(
        config => resInterceptor.onFulfilled(config, $message),
        error => resInterceptor.onRejected(error, $message)
    )
}

/**
 * 设置认证信息
 * @param auth {Object}
 */
function setAuthorization(auth) {
    Cookie.set(authHeader, 'Bearer ' + auth.token, {expires: auth.expireAt})
}

/**
 * 是否登录
 */
function isLogin() {
  let auth = Cookie.get(authHeader);
  return auth?true:false
}

/**
 * 登出
 */
function logout(){
  Cookie.remove(authHeader);
}

export {
    METHOD,
    request,
    initInterceptor,
    setAuthorization,
    requestWhitelistConfig,
    isLogin,
    logout
}