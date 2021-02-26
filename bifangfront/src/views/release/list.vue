
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
            <a-form-item>
              <a-button type="primary" @click.prevent="onCreateRelease">
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
          <a-button type="default" v-if="record.deploy_status == 29" disabled="true">
                已编译
          </a-button>
          <a-button type="primary" v-else @click="onBuild(record)">
                编译
          </a-button>
        </div>
        <template slot="statusTitle">
          <a-icon @click.native="onStatusTitleClick" type="info-circle" />
        </template>
      </bf-table>
    </div>
    <a-modal
      :visible="visiable"
      title="编译中"
      okText="确定"
      cancelText="关闭"
      @cancel="onReset"
      @ok="onReset"
    >
      <div style="text-align:center">
          <a-progress
            type="circle"
            :stroke-color="{
              '0%': '#108ee9',
              '100%': '#87d068',
            }"
            :percent="70"
          />
      </div>
    </a-modal>
  </a-card>
</template>

<script>
import BfTable from '@/components/table/table'
import API from '@/service'
import moment from 'moment'
const columns = [
  {
    title: '发布单编号',
    dataIndex: 'name'
  },
  {
    title: '项目',
    dataIndex: 'project_name'
  },
  {
    title: '组件',
    dataIndex: 'app_name'
  },
  {
    title: '编译分支',
    dataIndex: 'git_branch'
  },
  {

    title: '编译状态',
    dataIndex: 'deploy_status',
    slots: {title: 'statusTitle'},
    customRender: (status) => {return status == 29?'已编译': ' 未编译'}
  },
  {
    title: '用户',
    dataIndex: 'create_user_name'
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
      visiable:false,
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
        sort:""
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
      API.ReleaseList(this.params).then((res)=>{
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
    onBuild(data){
      this.visiable = true
      let params = {
        app_name: data.app,
        release_name: data.name,
        git_branch: data.git_branch
      }
      API.BuildRelease(params).then((res)=>{
        if(res.status == 200 ){
          this.$message.success("编译请中")
        }
        else{
          this.$message.error("编译请求失败~")
        }
      })
    },
    onReset(){
      this.visiable = false
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
    onCreateRelease(){
      this.$router.push("createRelease")
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

