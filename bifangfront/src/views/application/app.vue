
<template>
  <a-card>
    <div class="search">
      <a-form layout="inline" :form="form" @submit="submitHandler">
            <a-form-item
              label="应用名称"
            >
              <a-input 
              placeholder="请输入应用名称"
              v-decorator="['appName', { rules: [{ required: false, message: '请输入应用名称' }] }]" />
            </a-form-item>
            <a-form-item
              label="时间"
            >
              <a-range-picker
              v-decorator="['timePicker', {rules: [{ type: 'array', required: false }]}]" />
            </a-form-item>
            <a-form-item>
              <a-button type="primary" html-type="submit">
                查询
              </a-button>
            </a-form-item>
            <a-form-item>
              <a-button type="primary" @click.prevent="onCreateApp">
                新建
              </a-button>
            </a-form-item>
      </a-form>
    </div>
    <div>
      <bf-table
        :columns="columns"
        :dataSource="dataSource"
        rowKey="name"
        @clear="onClear"
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
        <div slot="description" slot-scope="{text}">
          {{text}}
        </div>
        <div slot="action" slot-scope="{text, record}">
          <a-button-group>
            <a-button type="primary" @click.prevent="onShowEdit(record)">
              编辑      
            </a-button>
            <a-popconfirm
              title="确定执行删除操作么？"
              ok-text="是"
              cancel-text="否"
              @confirm="onDelete(record)"
            >
              <a-button type="danger">
                删除      
              </a-button>
            </a-popconfirm>
          </a-button-group>
        </div>
      </bf-table>
    </div>
  </a-card>
</template>

<script>
import BfTable from '@/components/table/table'
import API from '@/service'
const columns = [
  {
    title: '应用ID',
    dataIndex: 'app_id'
  },
  {
    title: '应用名称',
    dataIndex: 'name'
  },
  {
    title: '中文名',
    dataIndex: 'cn_name'
  },
  {
    title: '归属项目',
    dataIndex: 'project_name',
  },
  {
    title: '启动用户',
    dataIndex: 'service_username'
  },
  {
    title: '服务端口',
    dataIndex: 'service_port'
  },
  {
    title: '更新时间',
    dataIndex: 'update_date',
    sorter: true
  },
  {
    title: '操作',
    scopedSlots: { customRender: 'action' }
  }
]

export default {
  name: 'module',
  components: {BfTable},
  data () {
    return {
      total:0,
      advanced: true,
      columns: columns,
      dataSource: [],
      selectedRows: [],
      params:{
        name:"",
        currentPage:1,
        pageSize:20,
        begin_time:"",
        end_time:"",
        sorter:""
      }
      
    }
  },
  beforeCreate() {
    this.form = this.$form.createForm(this, { name: 'moduleList' });
  },
  created(){
    this.fetchData()
  },
  methods: {
    toggleAdvanced () {
      this.advanced = !this.advanced
    },
    remove () {
      this.dataSource = this.dataSource.filter(item => this.selectedRows.findIndex(row => row.key === item.key) === -1)
      this.selectedRows = []
    },
    submitHandler(e){
      e.preventDefault()
      this.form.validateFields((err, fieldsValue) => {
          if (err) {
            return;
          }
          const rangeValue = fieldsValue['timePicker']
          this.params.name = fieldsValue["appName"]
          this.params.begin_time = rangeValue?rangeValue[0].format("YYYY-MM-DD"):""
          this.params.end_time = rangeValue?rangeValue[1].format("YYYY-MM-DD"):""
          this.fetchData()
        });
    },
    fetchData(){
      API.AppList(this.params).then((res)=>{
        let result = res.data
        if(res.status == 200 && result.code == 0){
          this.total = result.data.count
          this.dataSource = result.data.results;
        }
        else{
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
    onClear() {
      this.$message.info('您清空了勾选的所有行')
    },
    onStatusTitleClick() {
      this.$message.info('你点击了状态栏表头')
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
    },
    onCreateApp(){
      this.$router.push("appDetail")
    },
    onShowEdit(record){
      this.$router.push({
        path:"/application/appdetail",
        query:record
      })
    },
    onDelete(record){
      let {id} = record;
      if(id == undefined){
        this.$message.error("操作参数非法！")
        return false
      }
      API.DeleteApplication({id}).then((res)=>{
        let result = res.data
        if(res.status == 200 && result.code == 0){
          this.$message.success("删除成功~")
          this.fetchData()
        }
        else{
          this.$message.error("操作错误~:"+result.message)
        }
      })
    }
  }
}
</script>

<style lang="less" scoped>
  .search{
    margin-bottom: 10px;
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

