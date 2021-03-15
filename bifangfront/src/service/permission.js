import {request,METHOD} from '@/utils/request'
import {urlFormat} from '@/utils/util'
import {API} from './api'

/**
 * 获取权限列表
 * @param {*} params 
 */
async function PermissionList(params){

    return request(
        API.PERMISSIONLIST, 
        METHOD.GET,
        params
    )
}

/**
 * 新增权限
 * @param {*} params 
 */
async function CreatePermission(params){

    return request(
        API.CREATEPERMISSION, 
        METHOD.POST,
        params
    )
}

/**
 * 删除权限
 * @param {*} params 
 */
async function DeletePermission(params){
    const url = urlFormat(API.DELETEPERMISSION, params)
    return request(
        url, 
        METHOD.DELETE
    )
}


export default {
    PermissionList,
    CreatePermission,
    DeletePermission
}