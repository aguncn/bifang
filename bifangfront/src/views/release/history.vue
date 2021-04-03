
<template>
  <a-card>
    <div>
       <a-row>
         
        <a-col :span="11">
          <a-list item-layout="horizontal">
            <a-list-item >
              <a-list-item-meta
                :description=dataSource.id
              >
              <a slot="title">id</a>
              </a-list-item-meta>
            </a-list-item>
            <a-list-item >
              <a-list-item-meta
                :description=dataSource.name
              >
              <a slot="title">发布单号</a>
              </a-list-item-meta>
            </a-list-item>
            <a-list-item >
              <a-list-item-meta
                :description=dataSource.description
              >
              <a slot="title">描述</a>
              </a-list-item-meta>
            </a-list-item>
            <a-list-item >
              <a-list-item-meta
                :description=dataSource.project_name
              >
              <a slot="title">项目</a>
              </a-list-item-meta>
            </a-list-item>
            <a-list-item >
              <a-list-item-meta
                :description=dataSource.app_name
              >
              <a slot="title">应用</a>
              </a-list-item-meta>
            </a-list-item>
            <a-list-item >
              <a-list-item-meta
                :description=dataSource.create_user_name
              >
              <a slot="title">创建人</a>
              </a-list-item-meta>
            </a-list-item>
            <a-list-item >
              <a-list-item-meta
                :description=dataSource.env_name
              >
              <a slot="title">环境</a>
              </a-list-item-meta>
            </a-list-item>
            <a-list-item >
              <a-list-item-meta
                :description=dataSource.deploy_status_name
              >
              <a slot="title">状态</a>
              </a-list-item-meta>
            </a-list-item>
            <a-list-item >
              <a-list-item-meta
                :description= dataSource.git_url
              >
              <a slot="title">git服务器</a>
              </a-list-item-meta>
            </a-list-item>
            <a-list-item >
              <a-list-item-meta
                :description= dataSource.git_app_id
              >
              <a slot="title">git id</a>
              </a-list-item-meta>
            </a-list-item>
            <a-list-item >
              <a-list-item-meta
                :description=dataSource.git_branch
              >
              <a slot="title">git版本</a>
              </a-list-item-meta>
            </a-list-item>
            <a-list-item >
              <a-list-item-meta
                :description=dataSource.pipeline_url
              >
              <a slot="title">构建流水线url</a>
              </a-list-item-meta>
            </a-list-item>
            <a-list-item >
              <a-list-item-meta
                :description=dataSource.deploy_script_url
              >
              <a slot="title">部署脚本</a>
              </a-list-item-meta>
            </a-list-item>
            <a-list-item >
              <a-list-item-meta
                :description=dataSource.zip_package_url
              >
              <a slot="title">软件包</a>
              </a-list-item-meta>
            </a-list-item>
          </a-list>
        </a-col>
        <a-col :span="2">
        </a-col>
        <a-col :span="11">
          <a-timeline>
            <a-timeline-item color="blue" v-for="(item, index) in historyDataSource" :key="item.id">
              <a-icon slot="dot" type="clock-circle-o" style="font-size: 16px;" />
              <a-tag color='blue'>{{item.release_status_name}}</a-tag>
              
              <span v-show="item.release_status_name == 'Ready'">{{item.log}}</span>
              <a-tag>{{item.create_user}}</a-tag>
              {{item.create_date}} 
            </a-timeline-item>
          </a-timeline>         
        </a-col>
      </a-row>
    </div>
  </a-card>
</template>

<script>
import BfTable from '@/components/table/table'
import API from '@/service'
import moment from 'moment'

export default {
  name: 'releaseHistory',
  data () {
    return {
      releaseId: "",
      dataSource: {},
      historyDataSource: []
    }
  },
  created(){
    this.releaseId = this.$route.params.releaseId
    this.fetchReleaseData()
    this.fetchReleaseHistoryData()
  },
  methods: {
    fetchReleaseData(){
      API.ReleaseDetail(this.releaseId).then((res)=>{
        let result = res.data
        if(res.status == 200 && result.code == 0){
          this.dataSource = result.data;
        }
      })
    },
    fetchReleaseHistoryData(){
      let params = {
        release_id: this.releaseId
      }
      API.ReleaseHistory(params).then((res)=>{
        let result = res.data
        if(res.status == 200 && result.code == 0){
          this.historyDataSource = result.data.results;
          console.log(this.historyDataSource)
        }
      })
    }
  }
}
</script>

<style lang="less" scoped>
  .search{
    margin-bottom: 54px;
  }
  .fold{
    width: calc(100% - 216px);
    display: inline-block
  }
  .operator{
    margin-bottom: 18px;
  }
  @media screen and (max-width: 900px) {
    .fold {
      width: 100%;
    }
  }
</style>

