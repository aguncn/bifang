import {request,METHOD} from '@/utils/request'
import {API} from './api'

/**
 * 获取环境列表
 * @param {*} params 
 */
async function EnvList(params){

    return request(
        API.ENVLIST, 
        METHOD.GET,
        params
    )
}


export default {
    EnvList
}