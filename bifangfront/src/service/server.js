import {request,METHOD} from '@/utils/request'
import {urlFormat} from '@/utils/util'
import {API} from './api'

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

export default {
    ServerList,
    CreateServer,
    DeleteServer,
    UpdateServer
}