
<template>
  <a-card>
    <div class="search">
      <a-form layout="inline" :form="form" @submit="submitHandler">
            <a-form-item
              label="项目选择"
            >
            <a-select
                show-search
                placeholder="请选择项目"
                option-filter-prop="children"
                :filter-option="filterOption"
                @change="handleChange"
                style="width:200px"
                v-decorator="['projectId', { rules: [{ required: false, message: '请选择项目!' }] }]"
              >
                <a-select-option v-for="d in projectOption" :key="d">
                {{ d }}
                </a-select-option>
              </a-select>
            </a-form-item>
            <a-form-item
              label="组件选择"
            >
              <a-select
                show-search
                placeholder="请选择组件"
                option-filter-prop="children"
                :filter-option="filterOption"
                style="width:200px"
                v-decorator="['appId', { rules: [{ required: false, message: '请选择发布的组件!' }] }]"
              >
                <a-select-option v-for="d in options" :key="d.value">
                {{ d.label }}
                </a-select-option>
              </a-select>
            </a-form-item>
            <a-form-item
              label="发布单号"
            >
              <a-input 
              placeholder="请输入发布单"
              v-decorator="['releaseNo', { rules: [{ required: false, message: 'Please input your note!' }] }]" />
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
  name: 'deployList',
  components: {BfTable},
  data () {
    return {
      total:0,
      advanced: true,
      columns: columns,
      dataSource: [],
      projects:{},
      projectOption: [],
      options:[],
      params:{
        name:"",
        currentPage:1,
        pageSize:20,
        deploy_status: 'Ready,Ongoing,Failed,Success',
        sort:""
      }
    }
  },
  beforeCreate() {
    this.form = this.$form.createForm(this, { name: 'releaseList' });
  },
  created(){
    this.fetchAppList()
    this.fetchData()
  },
  methods: {
    toggleAdvanced () {
      this.advanced = !this.advanced
    },
    goDeploy(data){
			this.$router.push({ name: '发布单部署', params: { releaseId: data.id,  appId: data.app, envId: data.env}});
    },
    submitHandler(e){
      e.preventDefault()
      this.form.validateFields((err, fieldsValue) => {
          if (err) {
            return;
          }
          const rangeValue = fieldsValue['timePicker']
          this.params.name = fieldsValue["releaseNo"]
          this.params.projectName = fieldsValue["projectId"]
          this.params.appId = fieldsValue["appId"]
          this.fetchData()
        });
    },
    fetchData(){
      API.ReleaseList(this.params).then((res)=>{
        let result = res.data
        if(res.status == 200 && result.code == 0){
          this.total = result.data.count
          this.dataSource = result.data.results;
        } else {
          this.dataSource = []
        }
      })
    },
    fetchAppList(){
      API.AppList({}).then((res)=>{
        let result = res.data
        if(res.status == 200 && result.code == 0){
          result.data.results.forEach(item=>{
            this.projects[item.project_name]?
              this.projects[item.project_name].push({
              label:item.name,
              value:item.id
            }):this.projects[item.project_name] = [{
              label:item.name,
              value:item.id
            }]
          })
          this.projectOption = Object.keys(this.projects)
        }
        else{
          this.$message,error("无法获取应用列表~")
        }
      })
    },
    handleChange(value) {
      this.form.setFieldsValue({
        appId:""
      })
      this.options = this.projects[value]
    },
    filterOption(input, option) {
      return (
        option.componentOptions.children[0].text.toLowerCase().indexOf(input.toLowerCase()) >= 0
      );
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

