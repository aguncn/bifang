import {request,METHOD } from '@/utils/request'
import {urlFormat} from '@/utils/util'
import {API} from './api'


/**
 * 获取项目列表
 * @param {*} params 
 */
async function ProjectList(params){

    return request(
        API.PROJECTLIST, 
        METHOD.GET,
        params
    )
}

/**
 * 新增项目
 * @param {*} params 
 */
async function CreateProject(params){

    return request(
        API.CREATEPROJECT, 
        METHOD.POST,
        params
    )
}

/**
 * 删除项目
 * @param {*} params 
 */
async function DeleteProject(params){
    const url = urlFormat(API.DELETEPROJECT, params)
    return request(
        url, 
        METHOD.DELETE
    )
}

/**
 * 更新项目
 * @param {*} params 
 */
async function UpdateProject(params){
    const url = urlFormat(API.UPDATEPROJECT, params)
    return request(
        url, 
        METHOD.PUT,
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
    DeleteApplication,
    CreateApplication,
    UpdateApplication,
    ProjectList,
    CreateProject,
    DeleteProject,
    UpdateProject
}