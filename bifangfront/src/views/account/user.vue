
<template>
  <a-card>
    <div class="search">
      <a-form layout="inline" :form="form" @submit="submitHandler">
            <!-- <a-form-item
              label="组名称"
            >
              <a-input 
              placeholder="请输入组名称"
              v-decorator="['name', { rules: [{ required: false, message: 'Please input your note!' }] }]" />
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
            </a-form-item> -->
            <a-form-item>
              <a-button type="primary" @click.prevent="createDialog">
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
        <div slot="username" slot-scope="{text, record}">
          <a-tooltip>
          	<template slot="title">
          		{{record.url}}
          	</template>
          	  {{text}}
          </a-tooltip>
        </div>
        <template slot="groups_names" slot-scope="{text,record}">
          <a-tag color="blue" v-for="item in text">
            {{item.name}}
          </a-tag>
        </template>
        <template slot="email" slot-scope="{text,record}">
          <a-tag color='blue'>{{text}}</a-tag>
        </template>
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
        <template slot="statusTitle">
          <a-icon @click.native="onStatusTitleClick" type="info-circle" />
        </template>
      </bf-table>
    </div>
    <a-modal
      :visible="visible"
      :title="isEdit?'编辑账户组':'新增账户组'"
      :okText="isEdit?'更新':'新建'"
      @cancel="onReset"
      @ok="isEdit?onUpdateUser():onCreateUser()"
    >
      <a-form layout='vertical' :form="formDialog">
        <a-form-item
          label="ID"
          v-show="false"
        >
          <a-input placeholder="自动生成" 
            v-decorator="['id']"
          />
        </a-form-item>
        <a-form-item label='用户名'>
          <a-input
            v-decorator="[
              'username',
              {
                rules: [{ required: true, message: '请输入用户名' }],
              }
            ]"
          />
        </a-form-item>
        <a-form-item label='邮箱'>
          <a-input
            v-decorator="[
              'email',
              {
                rules: [{ required: true, message: '请输入邮箱' }],
              }
            ]"
          />
        </a-form-item>
        <a-form-item
          label="归属用户组"
        >
          <a-select
            show-search
            mode="multiple"
            placeholder="请选择归属用户组"
            option-filter-prop="children"
            style="min-width: 200px;width:100%"
            :filter-option="filterOption"
            v-decorator="['groups', { rules: [{ required: true, message: '请选择归属用户组!' }] }]"
          >
            <a-select-option v-for="d in options" :key="d.value">
            {{ d.label }}
            </a-select-option>
          </a-select>
        </a-form-item>
      </a-form>
    </a-modal>
  </a-card>
</template>

<script>
import BfTable from '@/components/table/table'
import API from '@/service'
const columns = [
  {
    title: '用户名',
    dataIndex: 'username',
    scopedSlots: {customRender: 'username'} 
  },
  {
    title: '所属用户组',
    dataIndex: 'groups_names',
    scopedSlots: {customRender: 'groups_names'} 
  },
  {
    title: '邮箱',
    dataIndex: 'email',
    scopedSlots: { customRender: 'email' }
  },
  {
    title: '操作',
    scopedSlots: { customRender: 'action' }
  }
]

export default {
  name: 'user',
  components: {BfTable},
  data () {
    return {
      total:0,
      advanced: true,
      columns: columns,
      dataSource: [],
      selectedRows: [],
      visible:false,
      options:[],
      isEdit:false,
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
    this.form = this.$form.createForm(this, { name: 'userList' });
    this.formDialog = this.$form.createForm(this, { name: 'formDialog' });
  },
  created(){
    this.fetchData()
    this.fetchGroupList()
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
          this.params.name = fieldsValue["name"]
          this.params.begin_time = rangeValue?rangeValue[0].format("YYYY-MM-DD"):""
          this.params.end_time = rangeValue?rangeValue[1].format("YYYY-MM-DD"):""
          this.fetchData()
        });
    },
    fetchData(){
      API.UserList(this.params).then((res)=>{
        let result = res.data
        if(res.status == 200 ){
          this.total = result.count
          this.dataSource = result.results;
          console.log(this.dataSource)
        }
        else{
          this.dataSource = []
        }
      })
    },
    onShowEdit(record){
      this.visible = true
      this.isEdit = true
      this.$nextTick(()=>{
        this.formDialog.setFieldsValue(record)
      })
    },
    onUpdateUser(){
      this.formDialog.validateFields((err, fieldsValue) => {
          if (err) {
            return;
          }
          let id = fieldsValue["id"],
              username = fieldsValue["username"],
              email = fieldsValue["email"],
              groups = fieldsValue["groups"];
          let data = {
            id,
            username,
            email,
            groups
          }
          API.UpdateUser(data).then((res)=>{
            let result = res.data
            if(res.status == 200){
              this.$message.success("用户组更新成功~")
              this.onReset()
              this.fetchData()
            }
            else{
              this.$message.error("用户组更新失败:"+result.message)
            }
          })
        })
    },
    onDelete(record){
      let {id} = record;
      if(id == undefined){
        this.$message.error("操作参数非法！")
        return false
      }
      API.DeleteUser({id}).then((res)=>{
        let result = res.data
        if(res.status == 204){
          this.$message.success("删除成功~")
          this.fetchData()
        }
        else{
          this.$message.error("操作错误~:"+result.message)
        }
      })
    },
    createDialog(){
      this.visible = true
    },
    onReset(){
      this.visible = false
      this.isEdit = false
      this.formDialog.resetFields()
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
    filterOption(input, option) {
      return (
        option.componentOptions.children[0].text.toLowerCase().indexOf(input.toLowerCase()) >= 0
      );
    },
    fetchGroupList(){
      API.GroupList({}).then((res)=>{
        let result = res.data
        if(res.status == 200){
          result.results.forEach(item=>{
            this.options.push({
              label:item.name,
              value:item.id
            })
          })
        }
        else{
          this.$message.error("无法获取用户组列表~")
        }
      })
    },
    onCreateUser () {
      this.formDialog.validateFields((err, fieldsValue) => {
          if (err) {
            return;
          }
          let data = fieldsValue;
          API.CreateUser(data).then((res)=>{
            let result = res.data
            if(res.status == 201){
              this.$message.success("用户组新增成功~")
              this.visible = false
              this.fetchData()
            }
            else{
              this.$message.error("用户组新增失败:"+result.message)
            }
          })
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

