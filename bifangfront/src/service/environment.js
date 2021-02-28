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

/**
 * 环境流转
 * @param {*} params 
 */
async function EnvExchange(params){

    return request(
        API.ENVEXCHANGE, 
        METHOD.POST,
        params
    )
}

export default {
    EnvList,
    EnvExchange
}