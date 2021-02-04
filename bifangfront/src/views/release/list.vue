
<template>
  <a-card>
    <div class="search">
      <a-form layout="inline" :form="form" @submit="submitHandler">
            <a-form-item
              label="发布单号"
            >
              <a-input 
              placeholder="请输入发布单"
              v-decorator="['releaseNo', { rules: [{ required: false, message: 'Please input your note!' }] }]" />
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
          <a style="margin-right: 8px">
            <a-icon type="plus"/>新增
          </a>
          <a style="margin-right: 8px">
            <a-icon type="edit"/>编辑
          </a>
        </div>
        <template slot="statusTitle">
          <a-icon @click.native="onStatusTitleClick" type="info-circle" />
        </template>
      </bf-table>
    </div>
  </a-card>
</template>

<script>
import BfTable from '@/components/table/table'
import { ReleaseList } from '@/service'
import moment from 'moment'
const columns = [
  {
    title: '发布单编号',
    dataIndex: 'name'
  },
  {
    title: '组件',
    dataIndex: 'app'
  },
  {
    title: '环境',
    dataIndex: 'env',
    customRender: (env) => {return env == 7?'UAT': ' 测试环境'}
  },
  {
    title: '编译分支',
    dataIndex: 'git_branch'
  },
  {
    title: '发布状态',
    dataIndex: 'deploy_status',
    slots: {title: 'statusTitle'},
    customRender: (status) => {return status == 29?'已发布': ' 未发布'}
  },
  {
    title: '更新时间',
    dataIndex: 'update_date',
    sorter: true,
    customRender: (date) =>{ return moment(date).format("YYYY-MM-DD hh:mm")}
  },
  {
    title: '操作',
    scopedSlots: { customRender: 'action' }
  }
]

export default {
  name: 'releaseList',
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
    this.form = this.$form.createForm(this, { name: 'releaseList' });
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
          this.params.name = fieldsValue["releaseNo"]
          this.params.begin_time = rangeValue?rangeValue[0].format("YYYY-MM-DD"):""
          this.params.end_time = rangeValue?rangeValue[1].format("YYYY-MM-DD"):""
          this.fetchData()
        });
    },
    fetchData(){
      ReleaseList(this.params).then((res)=>{
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
    addNew () {
      this.dataSource.unshift({
        key: this.dataSource.length,
        no: 'NO ' + this.dataSource.length,
        description: '这是一段描述',
        callNo: Math.floor(Math.random() * 1000),
        status: Math.floor(Math.random() * 10) % 4,
        updatedAt: '2018-07-26'
      })
    },
    handleMenuClick (e) {
      if (e.key === 'delete') {
        this.remove()
      }
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

