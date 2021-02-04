import {request,METHOD,requestWhitelistConfig } from '@/utils/request'

const BASE_URL = process.env.VUE_APP_API_BASE_URL;
const REAL_URL = process.env.VUE_APP_API_REAL_URL;
const API = {
    LOGIN: `${REAL_URL}/jwt_auth/`,
    REGISTER: `${REAL_URL}/account/register/`,
    RELEASELIST: `${REAL_URL}/release/list/`,
    APPLICATIONLIST: `${REAL_URL}/app/list/`,
    SERVERLIST: `${REAL_URL}/server/list/`,
    PROJECTIST: `${REAL_URL}/project/list/`,
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
 * 获取发布单列表
 * @param {*} params 
 */
async function ReleaseList(params){

    return request(
        API.RELEASELIST, 
        METHOD.GET,
        params
    )
}

/**
 * 获取应用列表
 * @param {*} params 
 */
async function AppList(params){

    return request(
        API.APPLICATIONLIST, 
        METHOD.GET,
        params
    )
}

/**
 * 获取项目列表
 * @param {*} params 
 */
async function ProjectList(params){

    return request(
        API.PROJECTIST, 
        METHOD.GET,
        params
    )
}

/**
 * 获取服务器列表
 * @param {*} params 
 */
async function ServerList(params){

    return request(
        API.SERVERLIST, 
        METHOD.GET,
        params
    )
}

export {
    API,
    Login,
    Register,
    ReleaseList,
    AppList,
    ProjectList,
    ServerList
}