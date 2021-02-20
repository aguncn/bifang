
<template>
  <a-card>
    <div class="search">
      <a-form layout="inline" :form="form" @submit="submitHandler">
            <a-form-item
              label="环境名称"
            >
              <a-input 
              placeholder="请输入环境名称"
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
            </a-form-item>
            <!-- <a-form-item>
              <a-button type="primary" @click.prevent="createDialog">
                新建
              </a-button>
            </a-form-item> -->
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
          <a style="margin-right: 8px" @click.prevent="onShowEdit(record)">
            <a-icon type="edit"/>编辑
          </a>
          <a style="margin-right: 8px" @click.prevent="onDelete(record)">
            <a-icon type="delete"/>删除
          </a>
        </div>
        <template slot="statusTitle">
          <a-icon @click.native="onStatusTitleClick" type="info-circle" />
        </template>
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
          label="名称"
          v-show="false"
        >
          <a-input placeholder="自动生成" 
            v-decorator="['id']"
          />
        </a-form-item>
        <a-form-item
          label="名称"
          v-show="isEdit"
        >
          <a-input placeholder="自动生成" 
            v-decorator="['serverName']"
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
            v-decorator="['appId', { rules: [{ required: true, message: '请选择发布的组件!' }] }]"
          >
            <a-select-option v-for="d in options" :key="d.value">
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
import { ServerList, EnvList, CreateServer, DeleteServer, UpdateServer } from '@/service'
import moment from 'moment'
const columns = [
  {
    title: '环境名称',
    dataIndex: 'name'
  },
  {
    title: '描述',
    dataIndex: 'description'
  },
  {
    title: '环境ID',
    dataIndex: 'env_id'
  },
  {
    title: 'salt',
    dataIndex: 'salt'
  },
  {
    title: '发布状态',
    dataIndex: 'base_status',
    customRender: (status) => {return status == true?'已发布': ' 未发布'}
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
  name: 'envList',
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
    this.form = this.$form.createForm(this, { name: 'envList' });
    this.formDialog = this.$form.createForm(this, { name: 'formDialog' });
  },
  created(){
    this.fetchData()
    this.fetchComponentList()
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
      EnvList(this.params).then((res)=>{
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
    onShowEdit(record){
      this.visible = true
      this.isEdit = true
      this.$nextTick(()=>{
        this.formDialog.setFieldsValue({
          id:record.id,
          serverName:record.name,
          ip:record.ip,
          port:record.port,
          system:record.system_type,
          appId:record.app,
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
              name = fieldsValue["serverName"],
              ip = fieldsValue["ip"],
              port = fieldsValue["port"],
              app_id = fieldsValue["appId"],
              system_type = fieldsValue["system"],
              description = fieldsValue["description"]||""
          let data = {
            id,
            name,
            ip,
            port,
            app_id,
            system_type,
            description
          }
          UpdateServer(data).then((res)=>{
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
      DeleteServer({id}).then((res)=>{
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
      EnvList({}).then((res)=>{
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
              system_type = fieldsValue["system"],
              description = fieldsValue["description"]||""
          let data = {
            name:[ip,'-', port].join(''),
            ip,
            port,
            app_id,
            system_type,
            description
          }
          CreateServer(data).then((res)=>{
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

