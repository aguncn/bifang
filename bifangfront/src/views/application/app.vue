
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
        <div slot="permission" slot-scope="{text, record}">
          <a-button @click.prevent="showPermission(record)">授权</a-button>
        </div>
        <div slot="action" slot-scope="{text, record}">
          <a-button-group>
            <a-button @click.prevent="onShowDetail(record)">
              查看      
            </a-button>
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
    
    <!---->
    <div>
      <a-drawer
        :title="`更新组件${selectApp}的权限`"
        :width="720"
        :visible="visible"
        :body-style="{ paddingBottom: '80px' }"
        @close="onClose"
      >
        <a-form :form="formPermission" layout="vertical" hide-required-mark>
          <a-row :gutter="16">
            <a-col :span="12">
              <a-form-item label="用户">
                <a-select
                  show-search
                  placeholder="用户"
                  option-filter-prop="children"
                  style="width: 320px"
                  @change="handleChange"
                  v-decorator="['selectUser', { rules: [{ required: true, message: '请选择授权用户!' }] }]"
                >
                  <a-select-option v-for="d in userOptions" :key="d.value">
                  {{ d.label }}
                  </a-select-option>
                </a-select>
              </a-form-item>
            </a-col>
            <a-col :span="12">
              <a-form-item label="操作">
                <a-button type="primary" @click.prevent="onCreatePermission('Create')" >
                  新建发布单
                </a-button>
                <a-button @click.prevent="onCreatePermission('Env')">环境流转</a-button>
                <a-button type="danger" @click.prevent="onCreatePermission('Deploy')">
                  部署
                </a-button>
              </a-form-item>
            </a-col>
          </a-row>
          <a-row :gutter="16">
            <a-col :span="24">
              <a-alert message="新建发布单权限" type="success" /><br/>
              <a-tag color="blue" v-for="item in createPermissionUser">
                <a-popconfirm
                    title="删除此用户权限?"
                    ok-text="确定"
                    cancel-text="否"
                    @confirm="confirmDeleteUser(item.id)"
                    @cancel="cancelDeleteUser"
                  >
                  {{item.name}}
                </a-popconfirm>
              </a-tag>
              <br/>
              <br/>
            </a-col>
            <a-col :span="24">
              <a-alert message="环境流转权限" type="success" /><br/>
              <a-tag color="blue" v-for="item in envPermissionUser">
                <a-popconfirm
                    title="删除此用户权限?"
                    ok-text="确定"
                    cancel-text="否"
                    @confirm="confirmDeleteUser(item.id)"
                    @cancel="cancelDeleteUser"
                  >
                  {{item.name}}
                </a-popconfirm>
              </a-tag>
              <br/>
              <br/>
            </a-col>
            <a-col :span="24">
              <a-alert message="部署权限" type="success" /><br/>
              <a-tag color="blue" v-for="item in deployPermissionUser">
                <a-popconfirm
                    title="删除此用户权限?"
                    ok-text="确定"
                    cancel-text="否"
                    @confirm="confirmDeleteUser(item.id)"
                    @cancel="cancelDeleteUser"
                  >
                  {{item.name}}
                </a-popconfirm>
              </a-tag>
              <br/>
              <br/>
            </a-col>
          </a-row>
        </a-form>
        <div
          :style="{
            position: 'absolute',
            right: 0,
            bottom: 0,
            width: '100%',
            borderTop: '1px solid #e9e9e9',
            padding: '10px 16px',
            background: '#fff',
            textAlign: 'right',
            zIndex: 1,
          }"
        >
          <a-button type="primary" @click="onClose">
            关闭
          </a-button>
        </div>
      </a-drawer>
    </div>
    <!---->
    <!--详情弹出框-->
    <a-modal
      :visible="detailVisible"
      :title="'应用详情'"
      :dialog-style="{ top: '30px' }"
      width="50%"
      okText="确定"
      :footer="null"
      @cancel="onDetailModalClose"
    >
      <a-card :border="false">
        <detail-list title="基础信息">
          <detail-list-item term="应用ID">{{detailRecord.app_id}}</detail-list-item>
          <detail-list-item term="应用名称">{{detailRecord.name}}</detail-list-item>
          <detail-list-item term="中文名">{{detailRecord.cn_name}}</detail-list-item>
          <detail-list-item term="归属项目">{{detailRecord.project_name}}</detail-list-item>
          <detail-list-item term="更新时间">{{dateTransformer(detailRecord.update_date)}}</detail-list-item>
          <a-row>
            <a-col :span="24">
              <detail-list-item term="应用描述">{{detailRecord.description}}</detail-list-item>
            </a-col>
          </a-row>
        </detail-list>
        <detail-list title="部署相关" >
          <detail-list-item term="GIT服务器">{{detailRecord.git_name}}</detail-list-item>
          <detail-list-item term="GIT项目ID">{{detailRecord.git_app_id}}</detail-list-item>
          <detail-list-item term="启动用户">{{detailRecord.service_username}}</detail-list-item>
          <detail-list-item term="服务端口">{{detailRecord.service_port}}</detail-list-item>
          <a-row>
            <a-col :span="24">
              <detail-list-item term="应用描述">{{detailRecord.description}}</detail-list-item>
            </a-col>
            <a-col :span="24">
              <detail-list-item term="Git Trigger Token">{{detailRecord.git_trigger_token}}</detail-list-item>
            </a-col>
            <a-col :span="24">
              <detail-list-item term="编译脚本">{{detailRecord.build_script}}</detail-list-item>
            </a-col>
            <a-col :span="24">
              <detail-list-item term="部署脚本">{{detailRecord.deploy_script}}</detail-list-item>
            </a-col>
            <a-col :span="24">
              <detail-list-item term="应用压缩包">{{detailRecord.zip_package_name}}</detail-list-item>
            </a-col>
          </a-row>
        </detail-list>
      </a-card>
    </a-modal>
    
    <!---->
    
  </a-card>
</template>

<script>
import moment from 'moment'
import BfTable from '@/components/table/table'
import DetailList from '@/components/tool/DetailList'
import API from '@/service'

const DetailListItem = DetailList.Item
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
    sorter: true,
    customRender: (date) =>{ return moment(date).format("YYYY-MM-DD hh:mm")}
  },
  {
    title: '权限',
    scopedSlots: { customRender: 'permission' }
  },
  {
    title: '操作',
    scopedSlots: { customRender: 'action' }
  }
]

export default {
  name: 'app',
  components: {BfTable,DetailList,DetailListItem},
  data () {
    return {
      total:0,
      visible: false,
      advanced: true,
      columns: columns,
      dataSource: [],
      userOptions: [],
      selectUser: "",
      selectApp: "",
      permissionDataSource: [],
      createPermissionUser: [],
      envPermissionUser: [],
      deployPermissionUser: [],
      selectedRows: [],
      detailVisible:false,
      detailRecord:{
        app_id:null,
        name:null,
        cn_name:null,
        project_name:null,
        description:null,
        git_name:null,
        git_app_id:null,
        git_trigger_token:null,
        build_script:null,
        deploy_script:null,
        zip_package_name:null,
        service_username:null,
        service_port:null,
        update_date:null
      },
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
    this.formPermission = this.$form.createForm(this, { name: 'permissionModuleList' });
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
    dateTransformer(date){
      return moment(date).format("YYYY-MM-DD hh:mm")
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
    fetchPermissionData(){
      let params = {
        "app": this.selectApp
      }
      API.PermissionList(params).then((res)=>{
        let result = res.data
        if(res.status == 200 && result.data.count > 0){
          this.total = result.data.count
          this.permissionDataSource = result.data.results;
           // 获取到所有APP的权限用户后，先清空，再按不同的权限，放入不同的用户列表中
          this.createPermissionUser = []
          this.envPermissionUser = []
          this.deployPermissionUser = []
          for (let elem of this.permissionDataSource.values()) {
            if (elem.action_name === "Create") {
              this.createPermissionUser.push({
                'id': elem.id,
                'name': elem.pm_username
              })
            }
            if (elem.action_name === "Env") {
              this.envPermissionUser.push({
                'id': elem.id,
                'name': elem.pm_username
              })
            }
            if (elem.action_name === "Deploy") {
              this.deployPermissionUser.push({
                'id': elem.id,
                'name': elem.pm_username
              })
            }
          }
        } else {
          this.permissionDataSource = []
          this.createPermissionUser = []
          this.envPermissionUser = []
          this.deployPermissionUser = []
        }
      })
    },
    onCreatePermission (param) {
      let action = param,
          user_id = this.selectUser,
          app_name = this.selectApp
      let data = {
        action,
        user_id,
        app_name
      }
      API.CreatePermission(data).then((res)=>{
        let result = res.data
        if(res.status == 200 && result.code == 0){
          this.$message.success("权限新增成功~")
          this.fetchPermissionData()
        }
        else{
          this.$message.error("权限新增失败:"+result.message)
        }
      })
    },
		fetchUser(){
		  API.UserList({}).then((res)=>{
		    let result = res.data
		    if(res.status == 200 && result.count > 0){
		      result.results.forEach(item=>{
		        this.userOptions.push({
		          label:item.username,
		          value:item.id
		        })
		      })
		    } else {
		      this.$message,error("无法获取用户列表~")
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
    onShowDetail(record){
      Object.assign(this.detailRecord,record)
      this.detailVisible = true
    },
    onDetailModalClose(){
      this.detailVisible = false
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
    },
    onClose() {
      this.visible = false;
    },
    handleChange(value) {
      this.selectUser = value
    },
    showPermission(record) {
      this.selectApp = record.name
      this.fetchUser()
      this.fetchPermissionData()
      this.visible = true
    },
    confirmDeleteUser(data) {
      let params = {"id": data}
      API.DeletePermission(params).then((res)=>{
        let result = res.data
        if(res.status == 200 && result.code == 0){
          this.$message.success("用户删除成功~")
          this.fetchPermissionData()
        }
        else{
          this.$message.error("用户删除操作错误~:"+result.message)
        }
      })
    },
    cancelDeleteUser() {
      this.$message.info('取消操作');
    },
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

