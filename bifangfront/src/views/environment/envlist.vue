
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
          <a-select
            show-search
            placeholder="环境"
            option-filter-prop="children"
            style="width: 80px"
            @change="handleChange"
            v-decorator="['appId', { rules: [{ required: true, message: '请选择发布的组件!' }] }]"
          >
            <a-select-option v-for="d in envOptions" :key="d.value">
            {{ d.label }}
            </a-select-option>
          </a-select>
          <a-popconfirm
          	:title="`是否将${record.name}发布单流转到${selectEnv}环境?`"
          	ok-text="是" 
          	cancel-text="否"
          	@confirm="envExchange(record)">
          	<a-button type="danger" >流转</a-button>
          </a-popconfirm>
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
    title: '环境',
    dataIndex: 'env_name'
  },
  {
    title: '操作',
    scopedSlots: { customRender: 'action' }
  }
]

export default {
  name: 'envList',
  components: {BfTable},
  data () {
    return {
      total:0,
      advanced: true,
      columns: columns,
      dataSource: [],
      envOptions:[],
      selectEnv: "",
      params:{
        name:"",
        currentPage:1,
        pageSize:20,
        begin_time:"",
        end_time:"",
        deploy_status: 'Build,Ready,Success',
        sort:""
      }
      
    }
  },
  beforeCreate() {
    this.form = this.$form.createForm(this, { name: 'releaseList' });
  },
  created(){
    this.fetchData()
    this.fetchEnv()
  },
  methods: {
    toggleAdvanced () {
      this.advanced = !this.advanced
    },
    handleChange(value) {
      this.selectEnv = value
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
          console.log(this.dataSource)
        } else {
          this.dataSource = []
        }
      })
    },
    fetchEnv(){
      API.EnvList({}).then((res)=>{
        let result = res.data
        if(res.status == 200 && result.code == 0){
          result.data.results.forEach(item=>{
            this.envOptions.push({
              label:item.name,
              value:item.name
            })
          })
        }
        else{
          this.$message,error("无法获取环境列表~")
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
    },
    envExchange(record) {
      let params = {
        env_name: this.selectEnv,
        release_name: record.name
      }
      console.log(params)
      API.EnvExchange(params).then((res)=>{
        if(res.status == 200 ){
          this.$message.success("环境流转完成，此发布单可以在指定环境进行部署。")
          this.fetchData()
        } else {
          this.$message.error("环境流转错误，请联系系统管理员~")
        }
      })
    },
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

