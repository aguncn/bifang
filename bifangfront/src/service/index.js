import {request,METHOD,requestWhitelistConfig } from '@/utils/request'
import {urlFormat} from '@/utils/util'

const BASE_URL = process.env.VUE_APP_API_BASE_URL;
const REAL_URL = process.env.VUE_APP_API_REAL_URL;
const API = {
    LOGIN: `${REAL_URL}/jwt_auth/`,
    REGISTER: `${REAL_URL}/account/register/`,
    RELEASELIST: `${REAL_URL}/release/list/`,
    APPLICATIONLIST: `${REAL_URL}/app/list/`,
    SERVERLIST: `${REAL_URL}/server/list/`,
    PROJECTIST: `${REAL_URL}/project/list/`,
    CREATERELEASE: `${REAL_URL}/release/create/`,
    CREATESERVER:`${REAL_URL}/server/create/`,
    DELETESERVER: `${REAL_URL}/server/delete/{{id}}/`,
    UPDATESERVER: `${REAL_URL}/server/update/{{id}}/`,
    CREATESUBJECT: `${REAL_URL}/project/create/`,
    DELETESUBJECT: `${REAL_URL}/project/delete/{{id}}/`,
    UPDATESUBJECT: `${REAL_URL}/project/update/{{id}}/`,
    DELETEAPPLICATION: `${REAL_URL}/app/delete/{{id}}/`,
    CREATEAPPLICATION: `${REAL_URL}/app/create/`,
    UPDATEAPPLICATION: `${REAL_URL}/app/update/{{id}}/`,
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

/**
 * 新建发布单
 * @param {*} params 
 */
async function CreateRelease(params){

    return request(
        API.CREATERELEASE, 
        METHOD.POST,
        params
    )
}

/**
 * 新增服务器
 * @param {*} params 
 */
async function CreateServer(params){

    return request(
        API.CREATESERVER, 
        METHOD.POST,
        params
    )
}

/**
 * 删除服务器
 * @param {*} params 
 */
async function DeleteServer(params){
    const url = urlFormat(API.DELETESERVER, params)
    return request(
        url, 
        METHOD.DELETE
    )
}

/**
 *更新服务器
 * @param {*} params 
 */
async function UpdateServer(params){
    const url = urlFormat(API.UPDATESERVER, params)
    return request(
        url, 
        METHOD.PUT,
        params
    )
}

/**
 * 新增项目
 * @param {*} params 
 */
async function CreateSubject(params){

    return request(
        API.CREATESUBJECT, 
        METHOD.POST,
        params
    )
}

/**
 * 删除项目
 * @param {*} params 
 */
async function DeleteSubject(params){
    const url = urlFormat(API.DELETESUBJECT, params)
    return request(
        url, 
        METHOD.DELETE
    )
}

/**
 *更新项目
 * @param {*} params 
 */
async function UpdateSubject(params){
    const url = urlFormat(API.UPDATESUBJECT, params)
    return request(
        url, 
        METHOD.PUT,
        params
    )
}

/**
 * 删除应用
 * @param {*} params 
 */
async function DeleteApplication(params){
    const url = urlFormat(API.DELETEAPPLICATION, params)
    return request(
        url, 
        METHOD.DELETE
    )
}

/**
 * 新增应用
 * @param {*} params 
 */
async function CreateApplication(params){

    return request(
        API.CREATEAPPLICATION, 
        METHOD.POST,
        params
    )
}

/**
 * 更新应用
 * @param {*} params 
 */
async function UpdateApplication(params){
    const url = urlFormat(API.UPDATEAPPLICATION, params)
    return request(
        url, 
        METHOD.PUT,
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
    ServerList,
    CreateRelease,
    CreateServer,
    DeleteServer,
    UpdateServer,
    CreateSubject,
    DeleteSubject,
    UpdateSubject,
    DeleteApplication,
    CreateApplication,
    UpdateApplication
}