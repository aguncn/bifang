
<template>
  <a-card>
    <div>
      <a-card type="inner" title="发布单信息">
        <detail-list size="small">
          <detail-list-item term="项目">{{ title.project_name }}</detail-list-item>
          <detail-list-item term="应用">
            {{ title.app_name }}
            <a :href="title.deploy_script_url" target="_blank">
              <a-tag color="blue">Build</a-tag>
            </a>
            <a :href="title.deploy_script_url" target="_blank">
              <a-tag color="green">Deploy</a-tag>
            </a>
          </detail-list-item>
          <detail-list-item term="环境">{{ title.env_name }}</detail-list-item>
          <detail-list-item term="发布单">{{ title.name }}</detail-list-item>
          <detail-list-item term="发布描述">{{ title.description }}</detail-list-item>
          <detail-list-item term="部署批次">{{ title.deploy_no }}</detail-list-item>
        </detail-list>
      </a-card>
      <a-table
        :columns="columns"
        :dataSource="dataSource"
        rowKey="ip"
        :row-selection="{ selectedRowKeys: selectedRow, onChange: onSelectChange }"
        @change="onChange"
        :pagination="{
          current: params.currentPage,
          pageSize: params.pageSize,
          total: total,
          showSizeChanger: true,
          showLessItems: true,
          showQuickJumper: true,
          showTotal: (total, range) => `第 ${range[0]}-${range[1]} 条，总计 ${total} 条`
        }"
      >
        <template slot="release_name" slot-scope="record">
          <a-tooltip>
          	<template slot="title">
          		{{ record.back_release_name }}
          	</template>
            <a-tag color='green' v-if="record.main_release_name===title.name">{{ record.main_release_name }}</a-tag>
          	<a-tag color='red' v-if="record.main_release_name!==title.name">{{ record.main_release_name }}</a-tag>
          </a-tooltip>
        </template>
        
        <template slot="server_log" slot-scope="text, record">
          <a-button type="primary" @click="logShow(record)">
            日志
          </a-button>
        </template>
      </a-table>
      <div class="alert">
        <a-alert type="info" style="line-height:2.4" :show-icon="true" v-if="selectedRow">
          <div class="message" slot="message">
            <a-row>
              <a-col :span="2">
                已选择&nbsp;<a>{{selectedRow.length}}</a>&nbsp;项 
              </a-col>
              <a-col :span="22">
                <a-popconfirm
                  title="确定执行回滚操作么？"
                  ok-text="是"
                  cancel-text="否"
                  @confirm="confirmRollback"
                >
                  <a-button type="primary" :disabled="selectedRow.length == 0" style="float:left">回滚</a-button>
                </a-popconfirm>
                <a-popconfirm
                  title="确定执行部署操作么？"
                  ok-text="是"
                  cancel-text="否"
                  @confirm="confirmDeploy"
                >
                  <a-button type="danger" :disabled="selectedRow.length == 0" style="float:right">部署</a-button>
                </a-popconfirm>
              </a-col>
            </a-row>
          </div>
        </a-alert>
      </div>
    </div>
    <a-modal
      :visible="visiableLog"
      title="服务器日志"
      okText="确定"
      cancelText="关闭"
      @cancel="onLogReset"
      @ok="onLogReset"
    >
      <a-card>
        <a-timeline>
          <div v-for="(item, index) in serverHistorySource" :key="item.id">
            <a-timeline-item color="blue" v-if="item.server==selectServer">
                <a-icon slot="dot" type="clock-circle-o" style="font-size: 16px;" />
                <a-tag color='blue'>{{item.server}}</a-tag>
                <a-tag >{{item.env}} {{item.release}} {{item.op_type}} {{item.action_type}}</a-tag><br/>
                {{item.log}}<br/>
                <a-tag color='green'>{{item.create_user}}</a-tag>
                {{item.create_date}}
                <a-badge :count="item.log_no" />
            </a-timeline-item>
          </div>
        </a-timeline>    
      </a-card>
    </a-modal>
    <a-modal
      :visible="visiableDeploy"
      :title="deployTitle"
      okText="确定"
      cancelText="关闭"
      @cancel="onDeployReset"
      @ok="onDeployReset"
    >
      <a-card>
        服务器列表：{{this.selectedRow}}<br/>
        <span v-if="deployResult === 'wait'">状态：部署中<a-icon type="sync"   :style="{ fontSize: '24px', color: '#00f' }" spin /><br/></span>
        <span v-else-if="deployResult === 'success'">状态：部署完成<a-icon type="check"   :style="{ fontSize: '24px', color: '#000' }" /> <br/></span>
        <span v-else>状态：部署出错，请查看服务器日志<a-icon type="close"   :style="{ fontSize: '24px', color: '#f00' }" /> <br/></span>
        输出记录：<span> {{deployLog}} <br/></span>
      </a-card>
    </a-modal>
  </a-card>
</template>

<script>
import BfTable from '@/components/table/table'
import DetailList from '@/components/tool/DetailList'
import API from '@/service'
import moment from 'moment'

const DetailListItem = DetailList.Item
const columns = [
  {
    title: 'IP_Port',
    dataIndex: 'name'
  },
  {
    title: '系统',
    dataIndex: 'system_type'
  },
  {
    title: '环境',
    dataIndex: 'env_name'
  },
  {
    title: '发布单',
    scopedSlots: { customRender: 'release_name' }
  },
  {
    title: '部署日志',
    scopedSlots: { customRender: 'server_log' }
  },
  {
    title: '更新时间',
    dataIndex: 'update_date',
    sorter: true,
    customRender: (date) =>{ return moment(date).format("YYYY-MM-DD hh:mm")}
  }
]
export default {
  name: 'serviceDeploy',
  components: {BfTable,DetailList,DetailListItem},
  data () {
    return {
      total: 0,
      visiableLog:false,
      visiableDeploy:false,
      releaseId: "",
      appId: "",
      envId: "",
      title: "",
      columns: columns,
      dataSource: [],
      serverHistorySource: [],
      selectServer: "",
      selectedRow:[],
      deployTitle: "",
      deployType: "",
      deployResult: "",
      deployLog: "",
      params:{
        currentPage:1,
        pageSize:20,
        sort:""
      }
    }
  },
  created(){
    this.releaseId = this.$route.query.releaseId
    this.appId = this.$route.query.appId
    this.envId = this.$route.query.envId
    this.fetchAllData()
  },
  methods: {
    fetchAllData(){
      this.fetchReleaseData()
      this.fetchServerData()
      
    },
    fetchReleaseData(){
      API.ReleaseDetail(this.releaseId).then((res)=>{
        let result = res.data
        if(res.status == 200 && result.code == 0){
          this.title =  result.data;
          this.fetchServerHistoryData()
        }
      })
    },
    fetchServerData(){
      let params = {
        app_id: this.appId,
        env_id: this.envId
      }
      API.ServerList(params).then((res)=>{
        if(res.status == 200 ){
          let result = res.data
          this.total = result.data.count
          this.dataSource = result.data.results;
        } else {
          this.dataSource = []
        }
      })
    },
    fetchServerHistoryData(){
      let params = {
        release_id: this.releaseId,
        env_id: this.envId,
        // 为了能演示此发布单在此环境的所有日志，注释掉部署批次，在详细服务器日志里识别
        //log_no: this.title.deploy_no,
        pageSize: 200
      }
      API.ServerHistory(params).then((res)=>{
        let result = res.data
        if(res.status == 200 && result.code == 0){
          this.serverHistorySource =  result.data.results
        }
      })
    },
    logShow(data){
      this.selectServer = data.name
      this.visiableLog = true
    },
    deployShow(data){
      this.selectServer = data.name
      this.visiableLog = true
    },
    onLogReset(){
      this.visiableLog = false
    },
    onDeployReset(){
      this.fetchAllData()
      this.deployResult = ""
      this.deployLog = ""
      this.visiableDeploy = false
      
    },
    onPageChange(page,pageSize){
      this.params.currentPage = page
      this.params.pageSize = pageSize
      this.fetchData()
    },
    onSizeChange(current, size) {
      this.params.currentPage = 1
      this.params.pageSize = size
      this.fetchData()
    },
    onSelectChange(selectedRowKeys,selectedRows) {
      this.selectedRow = selectedRowKeys;
    },
    confirmDeploy(e) {
      this.deployTitle = "部署"
      this.deployType = "deploy"
      this.onDeploy()
    },
    confirmRollback(e) {
      this.deployTitle = "回滚"
      this.deployType = "rollback"
      this.onDeploy()
    },
    onDeploy(){
      let params = {
        target_list: this.selectedRow.toString(),
        user_id: this.title.create_user,
        app_name: this.title.app_name,
        service_port: this.title.service_port,
        env_name: this.title.env_name,
        release_name: this.title.name,
        deploy_no: this.title.deploy_no,
        deploy_type: this.deployType,
        op_type: 'deploy',
      }
      this.deployResult = "wait"
      this.visiableDeploy = true
      API.Deploy(params).then((res)=>{
        console.log(res)
        if(res.data.code == 0 ){
          this.deployResult = "success"
        } else {
          this.deployResult = "failed"
        }
        this.deployLog = res.data.data
      })
    },
    onChange(pagination, filters, sorter) {
       console.log('Various parameters', pagination, filters, sorter);
       let {
         current,
         pageSize
       } = pagination
       let {
         order,
         field
       } = sorter
       this.params.currentPage = current
       this.params.pageSize = pageSize
       this.params.sorter = (field?field:"")
       this.fetchData()
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

