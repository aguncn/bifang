
<template>
  <a-card>
    <div>
      <a-button-group>
        <a-button type="primary">
          发布单信息
        </a-button>
        <a-button >
          项目：{{ title.project_name }}
        </a-button>
        <a-button >
          应用：{{ title.app_name }}
        </a-button>
        <a-button>
          环境：{{ title.env_name }}
        </a-button>
        <a-button >
          发布单：{{ title.name }}
        </a-button>
        <a-button >
          发布描述：{{ title.description }}
        </a-button>
      </a-button-group>
      <bf-table
        :columns="columns"
        :dataSource="dataSource"
        rowKey="name"
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
        <template slot="deploy_status_name" slot-scope="{text,record}">
          <a-tooltip>
          	<template slot="title">
          		{{record.description}}
          	</template>
          	<a-tag color='blue' v-if="text==='Ready'">准备就绪</a-tag>
            <a-tag color='green' v-if="text==='Success'">部署完成</a-tag>
            <a-tag color='orange' v-if="text==='Ongoing'">部署中...</a-tag>
            <a-tag color='red' v-if="text==='Failed'">部署异常</a-tag>
          </a-tooltip>
        </template>
        <div slot="action" slot-scope="{text, record}">
          <a-button type="primary" @click="goDeploy(record)">部署</a-button>
        </div>
      </bf-table>
    </div>
  </a-card>
</template>

<script>
import BfTable from '@/components/table/table'
import API from '@/service'
import moment from 'moment'

const columns = [
  {
    title: 'ip',
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
    title: '版本',
    dataIndex: 'main_release'
  },
  {
    title: '更新时间',
    dataIndex: 'update_date',
    sorter: true,
    customRender: (date) =>{ return moment(date).format("YYYY-MM-DD hh:mm")}
  },
  {
    title: '环境',
    dataIndex: 'env_name'
  },
  {
    title: '状态',
    dataIndex: 'deploy_status_name',
    scopedSlots: { customRender: 'deploy_status_name' }
  },
  {
    title: '操作',
    scopedSlots: { customRender: 'action' }
  }
]
export default {
  name: 'serviceDeploy',
  components: {BfTable},
  data () {
    return {
      total: 0,
      releaseId: "",
      appId: "",
      envId: "",
      title: "",
      columns: columns,
      dataSource: [],
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

