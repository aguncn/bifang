import {request,METHOD } from '@/utils/request'
import {urlFormat} from '@/utils/util'
import {API} from './api'


/**
 * 获取Git列表
 * @param {*} params 
 */
async function GitList(params){

    return request(
        API.GITLIST, 
        METHOD.GET,
        params
    )
}

export default {
    GitList
}