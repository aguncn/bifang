import {request,METHOD } from '@/utils/request'
import {urlFormat} from '@/utils/util'
import {API} from './api'

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

export default {
    AppList,
    ProjectList,
    DeleteApplication,
    CreateApplication,
    UpdateApplication,
}