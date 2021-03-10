
<template>
  <a-card>
    <div class="search">
      <a-form layout="inline" :form="form" @submit="submitHandler">
            <a-form-item
              label="服务器地址"
            >
              <a-input 
              placeholder="请输入服务器IP"
              v-decorator="['IP', { rules: [{ required: false, message: 'Please input your note!' }] }]" />
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
    <a-modal
      :visible="visible"
      :title="isEdit?'编辑服务器':'新增服务器'"
      :okText="isEdit?'更新':'新建'"
      @cancel="onReset"
      @ok="isEdit?onUpdateServer():onCreateServer()"
    >
      <a-form layout='vertical' :form="formDialog">
        <a-form-item
          label="id"
          v-show="false"
        >
          <a-input placeholder="自动生成" 
            v-decorator="['id']"
          />
        </a-form-item>
        <a-form-item label='服务器IP'>
          <a-input
            :disabled="isEdit?true:false"
            v-decorator="[
              'ip',
              {
                rules: [{ required: true, message: '请输入服务器IP' }],
              }
            ]"
          />
        </a-form-item>
        <a-form-item label='服务器端口'>
          <a-input
            :disabled="isEdit?true:false"
            v-decorator="[
              'port',
              {
                rules: [{ required: true, message: '请输入服务器端口' }],
              }
            ]"
          />
        </a-form-item>
        <a-form-item
          label="组件选择"
        >
          <a-select
            show-search
            placeholder="请选择组件"
            option-filter-prop="children"
            style="min-width: 200px;width:100%"
            :filter-option="filterOption"
            v-decorator="['appId', { rules: [{ required: true, message: '请选择所属的组件!' }] }]"
          >
            <a-select-option v-for="d in options" :key="d.value">
            {{ d.label }}
            </a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item
          label="环境选择"
        >
          <a-select
            show-search
            placeholder="请选择组件"
            option-filter-prop="children"
            style="min-width: 200px;width:100%"
            :filter-option="filterOption"
            v-decorator="['envId', { rules: [{ required: true, message: '请选择所属的环境!' }] }]"
          >
            <a-select-option v-for="d in envOptions" :key="d.value">
            {{ d.label }}
            </a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item 
          label="操作系统"
        >
          <a-select
            v-decorator="[ 'system', { rules: [{ required: true, message: '请选择操作系统' }] }]"
          >
            <a-select-option value="WINDOWS">
              WINDOWS
            </a-select-option>
            <a-select-option value="LINUX">
              LINUX
            </a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label='描述'>
          <a-input
            type='textarea'
            v-decorator="['description']"
          />
        </a-form-item>
      </a-form>
    </a-modal>
  </a-card>
</template>

<script>
import BfTable from '@/components/table/table'
import API from '@/service'
import moment from 'moment'
const columns = [
  {
    title: '服务器IP',
    dataIndex: 'name'
  },
  {
    title: '端口',
    dataIndex: 'port'
  },
  {
    title: '系统类型',
    dataIndex: 'system_type'
  },
  {
    title: '所属应用',
    dataIndex: 'app_name'
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
  },
  {
    title: '操作',
    scopedSlots: { customRender: 'action' }
  }
]

export default {
  name: 'serverList',
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
      envOptions:[],
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
    this.form = this.$form.createForm(this, { name: 'serverList' });
    this.formDialog = this.$form.createForm(this, { name: 'formDialog' });
  },
  created(){
    this.fetchData()
    this.fetchComponentList()
    this.fetchEnv()
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
          this.params.name = fieldsValue["IP"]
          this.params.begin_time = rangeValue?rangeValue[0].format("YYYY-MM-DD"):""
          this.params.end_time = rangeValue?rangeValue[1].format("YYYY-MM-DD"):""
          this.fetchData()
        });
    },
    fetchData(){
      API.ServerList(this.params).then((res)=>{
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
    fetchEnv(){
      API.EnvList({}).then((res)=>{
        let result = res.data
        if(res.status == 200 && result.code == 0){
          result.data.results.forEach(item=>{
            this.envOptions.push({
              label:item.name,
              value:item.id
            })
          })
        }
        else{
          this.$message,error("无法获取环境列表~")
        }
      })
    },
    onShowEdit(record){
      this.visible = true
      this.isEdit = true
      this.$nextTick(()=>{
        this.formDialog.setFieldsValue({
          id:record.id,
          ip:record.ip,
          port:record.port,
          system:record.system_type,
          appId:record.app,
          envId:record.env,
          description:record.description
        })
      })
    },
    onUpdateServer(){
      this.formDialog.validateFields((err, fieldsValue) => {
          if (err) {
            return;
          }
          let id = fieldsValue["id"],
              ip = fieldsValue["ip"],
              port = fieldsValue["port"],
              app_id = fieldsValue["appId"],
              env_id = fieldsValue["envId"],
              system_type = fieldsValue["system"],
              description = fieldsValue["description"]||""
          let data = {
            id,
            ip,
            port,
            app_id,
            env_id,
            system_type,
            description
          }
          API.UpdateServer(data).then((res)=>{
            let result = res.data
            if(res.status == 200){
              this.$message.success("服务器更新成功~")
              this.onReset()
              this.fetchData()
            }
            else{
              this.$message.error("服务器更新失败:"+result.message)
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
      API.DeleteServer({id}).then((res)=>{
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
    fetchComponentList(){
      API.AppList({}).then((res)=>{
        let result = res.data
        if(res.status == 200 && result.code == 0){
          result.data.results.forEach(item=>{
            this.options.push({
              label:item.name,
              value:item.id
            })
          })
        }
        else{
          this.$message.error("无法获取应用列表~")
        }
      })
    },
    onCreateServer () {
      this.formDialog.validateFields((err, fieldsValue) => {
          if (err) {
            return;
          }
          let ip = fieldsValue["ip"],
              port = fieldsValue["port"],
              app_id = fieldsValue["appId"],
              env_id = fieldsValue["envId"],
              system_type = fieldsValue["system"],
              description = fieldsValue["description"]||""
          let data = {
            ip,
            port,
            app_id,
            env_id,
            system_type,
            description
          }
          API.CreateServer(data).then((res)=>{
            let result = res.data
            if(res.status == 200 && result.code == 0){
              this.$message.success("服务器新增成功~")
              this.visible = false
              this.fetchData()
            }
            else{
              this.$message.error("服务器新增失败:"+result.message)
            }
          })
        })
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

