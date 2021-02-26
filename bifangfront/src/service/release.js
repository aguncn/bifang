import {request,METHOD} from '@/utils/request'
import {API} from './api'

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
 * 编译发布单
 * @param {*} params 
 */
async function BuildRelease(params){

    return request(
        API.RELEASEBUILD, 
        METHOD.POST,
        params
    )
}

export default {
    ReleaseList,
    CreateRelease,
    BuildRelease
}