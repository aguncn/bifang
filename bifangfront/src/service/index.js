import {request,METHOD,requestWhitelistConfig } from '@/utils/request'

const BASE_URL = process.env.VUE_APP_API_BASE_URL;
const REAL_URL = process.env.VUE_APP_API_REAL_URL;
const API = {
    LOGIN: `${REAL_URL}/jwt_auth/`,
    REGISTER: `${REAL_URL}/account/register/`,
    RELEASELIST: `${REAL_URL}/release/list/`
}

requestWhitelistConfig([
    API.LOGIN,
    API.REGISTER
])

/**
 * 登录
 * @param {*} params 
 */
async function Login(params){
    let {username,password} = params

    return request(
        API.LOGIN, 
        METHOD.POST,
        {
            username,
            password
        }
    )
}

/**
 * 注册
 * @param {*} params 
 */
async function Register(params){
    let {
        username = '',
        password = '',
        passwordConfirm = '',
        email = ''
    } = params;

    return request(
        API.REGISTER, 
        METHOD.POST,
        {
            username,
            password,
            passwordConfirm,
            email
        }
    )
}

/**
 * 获取发布单
 * @param {*} params 
 */
async function ReleaseList(){

    return request(
        API.RELEASELIST, 
        METHOD.GET
    )
}

export {
    API,
    Login,
    Register,
    ReleaseList
}