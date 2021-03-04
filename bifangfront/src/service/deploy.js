import {request,METHOD} from '@/utils/request'
import {API} from './api'

/**
 * 部署软件
 * @param {*} params 
 */
async function Deploy(params){

    return request(
        API.DEPLOY, 
        METHOD.POST,
        params
    )
}

export default {
    Deploy
}