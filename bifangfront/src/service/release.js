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
 * 获取发布单详情
 * @param {*} params 
 */
async function ReleaseDetail(params){
    URL = `${API.RELEASEDETAIL}${params}/`
    console.log(URL)
    return request(
        URL, 
        METHOD.GET
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

/**
 * 获取发布单编译进度和状态
 * @param {*} params 
 */
async function BuildReleaseStatus(params){
  return request(
      API.RELEASEBUILDSTATUS, 
      METHOD.POST,
      params
  )
}

export default {
    ReleaseList,
    ReleaseDetail,
    CreateRelease,
    BuildRelease,
    BuildReleaseStatus
}