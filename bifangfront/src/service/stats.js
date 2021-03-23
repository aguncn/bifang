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

async function ReleaseTop5(){
  return request(
      API.RELEASETOP5, 
      METHOD.GET,
  )
}

async function ReleaseFailedTop5(){
  return request(
      API.RELEASEFAILEDTOP5, 
      METHOD.GET,
  )
}

export default {
  AllCount,
  ReleaseTop5,
  ReleaseFailedTop5
}