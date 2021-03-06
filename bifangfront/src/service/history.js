import {request,METHOD} from '@/utils/request'
import {API} from './api'

/**
 * 获取发布单历史操作
 * @param {*} params 
 */
async function ReleaseHistory(params){
  return request(
      API.RELEASEHISTORY, 
      METHOD.GET,
      params
  )
}

/**
 * 获取服务器历史操作
 * @param {*} params 
 */
async function ServerHistory(params){
  return request(
      API.SERVERHISTORY, 
      METHOD.GET,
      params
  )
}


export default {
    ReleaseHistory,
    ServerHistory
}