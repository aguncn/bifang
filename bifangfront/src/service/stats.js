import {request,METHOD} from '@/utils/request'
import {urlFormat} from '@/utils/util'
import {API} from './api'

/**
 * 获取项目，应用，发布单总数
 */
async function AllCount(){
  return request(
      API.ALLCOUNT, 
      METHOD.GET,
  )
}

export default {
  AllCount
}