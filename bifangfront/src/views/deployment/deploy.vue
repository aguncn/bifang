
<template>
  <a-card>
    <div>
      <a-card type="inner" title="发布单信息">
        <detail-list size="small">
          <detail-list-item term="项目">{{ title.project_name }}</detail-list-item>
          <detail-list-item term="应用">{{ title.app_name }}</detail-list-item>
          <detail-list-item term="环境">{{ title.env_name }}</detail-list-item>
          <detail-list-item term="发布单">{{ title.name }}</detail-list-item>
          <detail-list-item term="发布描述">{{ title.description }}</detail-list-item>
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
      </a-table>
      <div class="alert">
        <a-alert type="info" style="line-height:2.4" :show-icon="true" v-if="selectedRow">
          <div class="message" slot="message">
            已选择&nbsp;<a>{{selectedRow.length}}</a>&nbsp;项 
            <a-button type="danger" style="float:right" @click="onDeploy">部署</a-button>
          </div>
        </a-alert>
      </div>
    </div>
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
    title: 'IP',
    dataIndex: 'ip'
  },
  {
    title: '端口',
    dataIndex: 'port'
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
      releaseId: "",
      appId: "",
      envId: "",
      title: "",
      columns: columns,
      dataSource: [],
      selectedRow:[],
      deploySelectedRows:[],
      params:{
        currentPage:1,
        pageSize:20,
        sort:""
      }
    }
  },
  created(){
    this.releaseId = this.$route.params.releaseId
    this.appId = this.$route.params.appId
    this.envId = this.$route.params.envId
    this.fetchReleaseData()
    this.fetchServerData()
    
  },
  methods: {
    fetchReleaseData(){
      API.ReleaseDetail(this.releaseId).then((res)=>{
        let result = res.data
        if(res.status == 200 && result.code == 0){
          this.title =  result.data;
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
      this.deploySelectedRows = selectedRows
    },
    onDeploy(){
      console.log("3:", this.deploySelectedRows)
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

