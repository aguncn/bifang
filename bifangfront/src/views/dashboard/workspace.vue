<template>
<div>
    <a-card :bordered="false">
      <div style="display: flex; flex-wrap: wrap">
          <head-info title="项目数量" :content="allCount.projectCount+'个'" :bordered="true"/>
          <head-info title="应用数量" :content="allCount.appCount+'个'" :bordered="true"/>
          <head-info title="发布单数量" :content="allCount.releaseCount+'个'"/>
      </div>
    </a-card>
        
        <a-row style="margin-top:20px">
            <a-col style="padding-right:2px" :xl="16" :lg="24" :md="24" :sm="24" :xs="24">
                <a-card title="全景图" :bordered="false">
                    <my-echarts />
                </a-card>
                <a-card class="project-list" style="margin: 12px 0;" :bordered="false" title="项目" :body-style="{padding: 0}">
                    <a href="#/application/project" slot="extra">全部项目</a>
                    <div>
                    <a-card-grid :key="i" v-for="(item, i) in projectData">
                        <a-card :bordered="false" :body-style="{padding: 0}">
                        <a-card-meta :description="item.description">
                            <div slot="title" class="card-title">
                            <a-avatar size="small" :src="item.logo" />
                            <span>{{item.cn_name}}</span>
                            </div>
                        </a-card-meta>
                        <div class="project-item">
                            <a class="group" href="/#/">{{item.create_user_name}}</a>
                            <span class="datetime">{{item.time}}</span>
                        </div>
                        </a-card>
                    </a-card-grid>
                    </div>
                </a-card>
            </a-col>
            <a-col style="padding-left: 12px" :xl="8" :lg="24" :md="24" :sm="24" :xs="24">
            <a-card title="快捷入口" style="margin-bottom: 24px" :bordered="false" :body-style="{padding: 0}">
                <div class="item-group">
                <a-tag color="red">
                    <a href="#/release/releaseList">发布单列表</a>
                </a-tag>
                <a-tag color="green">
                    <a href="#/release/createRelease">创建发布单</a>
                </a-tag>
                <a-tag color="blue">
                    <a href="#/deployment/deploy">服务部署</a>
                </a-tag><br/>
                <a-tag color="blue">
                    <a href="#/application/app">添加组件</a>
                </a-tag>
                <a-tag color="green">
                    <a href="#/application/project">添加项目</a>
                </a-tag>
                </div>
            </a-card>
            <a-card title="运行动态" style="margin-bottom: 24px" :bordered="false">
                <div style="min-height: 400px;">
                <a-list>
                <a-list-item :key="index" v-for="(item, index) in releaseData">
                    <a-list-item-meta>
                    <a-avatar slot="avatar" :src="item.avatar" />
                    <div slot="title" v-html="item.action" />
                    <div slot="description">{{item.time}}</div>
                    </a-list-item-meta>
                </a-list-item>
                </a-list>
                </div>
            </a-card>
            </a-col>
        </a-row>
</div>
</template>
<script>
import HeadInfo from '@/components/tool/headInfo'
import MyEcharts from '@/components/tool/myEcharts'
import API from '@/service'
import moment from 'moment'

const projectIcons = [
    'https://gw.alipayobjects.com/zos/rmsportal/WdGqmHpayyMjiEhcKoVE.png',
    'https://gw.alipayobjects.com/zos/rmsportal/zOsKZmFRdUtvpqCImOVY.png',
    'https://gw.alipayobjects.com/zos/rmsportal/dURIMkkrRFpPgTuzkwnB.png'
]

const avatars = [
  'https://gw.alipayobjects.com/zos/rmsportal/cnrhVkzwxjPwAaCfPbdc.png',
  'https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png',
  'https://gw.alipayobjects.com/zos/rmsportal/gaOngJwsRYRaVAuXXcmB.png',
  'https://gw.alipayobjects.com/zos/rmsportal/WhxKECPNujWoWEFNdnJE.png',
  'https://gw.alipayobjects.com/zos/rmsportal/ubnKSIfAJTxIgXOKlciN.png',
  'https://gw.alipayobjects.com/zos/rmsportal/jZUIxmJycoymBprLOUbT.png'
]

export default {
    name:"dashboard",
    components: {HeadInfo,MyEcharts},
    created(){
        this.fetchReleaseData()
        this.fetchProjectData()
        this.fetchAllCount()
    },
    data(){
        return {
            allCount:{},
            releaseData:[],
            projectData:[]
        }
    },
    methods:{
      fetchAllCount(){
        API.AllCount().then((res)=>{
            let result = res.data
            if(res.status == 200 && result.code == 0){
              // 后端传过来的是一个Json对象
              this.allCount.projectCount = result.data.project
              this.allCount.appCount = result.data.app
              this.allCount.releaseCount = result.data.release
            } else {
                this.allCount = {}
            }
        })
      },
      fetchProjectData(){
        let param = {
            currentPage: 1,
            pageSize: 6,
            sort: '-update_date'
        }
        API.ProjectList(param).then((res)=>{
            let result = res.data
            if(res.status == 200 && result.code == 0){
                this.projectTotal = result.data.count
                result.data.results.forEach(item=>{
                    this.projectData.push({
                        ...item,
                        logo: projectIcons[Math.floor(Math.random()*10)%3],
                        time:this.formatTime(item.update_date)
                    })
                })
            }
            else{
                this.projectData = []
            }
        })
      },
      fetchReleaseData(){
        let params = {
            currentPage:1,
            pageSize:5,
            sort:"-update_date"
        }
        API.ReleaseList(params).then((res)=>{
            let result = res.data
            if(res.status == 200 && result.code == 0){
                this.releaseTotal = result.data.count
                result.data.results.forEach(item=>{
                    this.releaseData.push({
                        avatar: avatars[Math.floor(Math.random()*10)%4],
                        user:item.create_user_name,
                        name:item.name,
                        action:this.actionTranformer(item.create_user_name,item.release_status_name,item.name),
                        time: this.formatTime(item.update_date)
                    })
                })
            } else {
                this.releaseData = []
            }
        })
      },
      formatTime(time){
          let str = "";
          let current = moment(),
              date = moment(time),
              du = moment.duration(current-date,'ms'),
              days = du.get('days'),
              hours = du.get('hours'),
              mins = du.get('minutes');
          if(days > 0){
              str = days+"天之前"
          }
          else if(hours > 0){
              str = hours+"小时之前"
          }
          else{
              str = mins+"分钟之前"
          }
          return str
      },
      actionTranformer(username,status,releaseNo){
          let action=""
          let release = `<a href="#/release/releaseList">${releaseNo}</a>`
          switch(status.toLowerCase()){
              case "create":
                  action=`${username} 新建发布单${release}`
                  break;
              case "build":
                  action=`${username} 构建发布单${release}`
                  break;
              case "ready":
                  action=`${username} 扭转发布单${release}`
                  break;
              case "success":
                  action=`${username} 部署发布单${release}成功`
                  break;
              case "failed":
                  action=`${username} 部署发布单${release}失败`
                  break;
              case "ongoing":
                  action=`${username} 发布单${release}部署中`
                  break;
              default:
                  action=`${username} 操作发布单${release}`
                  break;
          }
          return action
      }
    }
}
</script>
<style lang="less">
.project-list {
  .card-title {
    span{
      vertical-align: middle;
      &:last-child{
        margin-left: 12px;
      }
    }
  }
  .project-item {
    display: flex;
    justify-content: space-between;
    margin-top: 8px;
    overflow: hidden;
    font-size: 12px;
    color: inherit;
    .group{
      color: @bf-text-color;
      flex: 1 1 0;
      &:hover {
        color: @bf-primary-color;
      }
    }
    .datetime {
      color: @bf-text-color-second;
      flex: 0 0 auto;
    }
  }
  .ant-card-meta-description {
    height: 44px;
    line-height: 22px;
    overflow: hidden;
  }
}
.item-group{
  padding: 20px 0 8px 24px;
  font-size: 0;
  span {
      margin: 5px;
  }
  a{
    color: inherit;
    display: inline-block;
    font-size: 14px;
    margin-bottom: 13px;
    width: 25%;
  }
}
.members {
  a {
    display: block;
    margin: 12px 0;
    color: @bf-text-color;
    &:hover {
      color: @bf-primary-color;
    }
    .member {
      vertical-align: middle;
      margin-left: 12px;
    }
  }
}

</style>
