
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
                v-decorator="['projectName', { rules: [{ required: false, message: '请选择项目!' }] }]"
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
        <div slot="name" slot-scope="{text, record}">
          <a-tooltip>
          	<template slot="title">
          		{{record.description}}
          	</template>
          	<a @click="showReleaseHistory(record)">
          	  {{text}}
          	</a>
          </a-tooltip>
        </div>
        <div slot="action" slot-scope="{text, record}">
          <a-button type="primary" v-if="record.deploy_status_name == 'Create'" @click="buildShow(record)">
            构建      
          </a-button>
          <a-button type="primary" v-else-if="record.deploy_status_name == 'BuildFailed'" @click="buildShow(record)">
            构建
          </a-button>
          <a-button type="default" v-else  disabled>
            已构建   
          </a-button>
        </div>
        <template slot="git_branch" slot-scope="{text,record}">
          <a-tooltip>
          	<template slot="title">
          		{{record.description}}
          	</template>
          	<a-tag color='blue'>{{text}}</a-tag>
          </a-tooltip>
        </template>
        <template slot="statusTitle">
          <a-icon @click.native="onStatusTitleClick" type="info-circle" />
        </template>
      </bf-table>
    </div>
    <a-modal
      :visible="visiable"
      title="软件构建"
      okText="确定"
      cancelText="关闭"
      @cancel="onReset"
      @ok="onReset"
    >
      <a-card>
        <p>发布单: {{this.modelData.name}}</p>
        <p>app: {{this.modelData.app_name}}</p>
        <p>git地址: {{this.modelData.git_url}}/{{this.modelData.project_name}}/{{this.modelData.app_name}}</p>
        <p>git 项目ID: {{this.modelData.git_app_id}}</p>
        <p>代码分支: {{this.modelData.git_branch}}</p>
        <div v-if="buildStatus == 'notBegin'">
          <p>构建状态: 尚未开始</p>
          <a-button type="danger" @click="onBuild">开始构建</a-button>
        </div>
        <div v-else-if="buildStatus == 'building'">
          <p>构建状态: 构建中，请等候<a-icon type="sync" :style="{ fontSize: '24px', color: '#00f' }" spin /></p>
        </div>
        <div v-else-if="buildStatus == 'failed'">
          <p>构建状态: 构建失败，请调整后重试。<a-icon type="close" :style="{ fontSize: '24px', color: '#f00' }" /></p>
          <a-button type="danger" @click="onBuild">开始构建</a-button>
        </div>
        <div v-else>
          <p>构建状态: 构建完成，如有权限，可操作流转。<a-icon type="check" :style="{ fontSize: '24px', color: '#000' }" /></p>
          <a-button type="danger" @click="onSwitch">快速环境流转</a-button>
        </div>
      </a-card>
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
    dataIndex: 'name',
    scopedSlots: {customRender: 'name'} 
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
  	dataIndex: 'git_branch',
    scopedSlots: {customRender: 'git_branch'} 
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
      modelData: {},
      buildTimer: null, 
      buildStatus: "notBegin",
      advanced: true,
      columns: columns,
      dataSource: [],
      selectedRows: [],
      projects:{},
      projectOption: [],
      options:[],
      params:{
        name:"",
        currentPage:1,
        pageSize:20,
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
  destroyed(){
    this.clearBuildTimer()
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
          this.params.project_name = fieldsValue["projectName"]
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
          console.log(this.dataSource)
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
    showReleaseHistory(data) {
      console.log(data)
    	//链接到发布单历史部署详细页面
    	this.$router.push({ name: '发布单部署历史', params: { releaseId: data.id }});
    },
    buildShow(data){
      this.modelData = data
      this.visiable = true
    },
    onSwitch(){
      this.$router.push({
        path:'/environment/environmentList',
        query:{
          releaseNo: this.modelData.name
        }
      })
    },
    onBuild(){
      let params = {
        app_name: this.modelData.app_name,
        release_name: this.modelData.name,
        git_branch: this.modelData.git_branch
      }
      API.BuildRelease(params).then((res)=>{
        if(res.status == 200 ){
          this.$message.success("开始构建......")
          this.getBuildStatus()
        } else {
          this.$message.error("构建请求失败~")
        }
      })
    },
    getBuildStatus() {
      this.buildTimer = setInterval(() => {  //创建定时器
          let params = {
            app_name: this.modelData.app_name,
            release_name: this.modelData.name
          }
          API.BuildReleaseStatus(params).then((res)=>{
            if(res.status != 200 ){
              console.log(res, "no 200")
              this.buildTimer && this.clearBuildTimer(); // 关闭定时器
            } else {
              let resData = res.data.data
              if(resData == "ing" ){
                this.buildStatus = 'building'
              } else if (resData == "success" ) {
                this.buildStatus = 'success'
                console.log(resData)
                this.buildTimer && this.clearBuildTimer();
              } else {
                this.buildStatus = 'failed'
                console.log(resData)
                this.buildTimer && this.clearBuildTimer();
              }
            }
          })
      }, 3000);
    },
    clearBuildTimer() {//清除定时器
      clearInterval(this.buildTimer);
      this.buildTimer = null;
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

