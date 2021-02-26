
<template>
  <a-card>
    <div class="search">
      <a-form layout="inline" :form="form" @submit="submitHandler">
            <a-form-item
              label="项目名称"
            >
              <a-input 
              placeholder="请输入项目名"
              v-decorator="['projectName', { rules: [{ required: false, message: 'Please input your note!' }] }]" />
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
      :title="isEdit?'编辑项目':'新增项目'"
      :okText="isEdit?'更新':'新建'"
      @cancel="onReset"
      @ok="isEdit?onUpdateSubject():onCreateSubject()"
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
        <a-form-item label='英文名称'>
          <a-input
            :disabled="isEdit?true:false"
            v-decorator="[
              'name',
              {
                rules: [{ required: true, message: '请输入英文名称' }],
              }
            ]"
          />
        </a-form-item>
        <a-form-item label='中文名称'>
          <a-input
            v-decorator="[
              'cnname',
              {
                rules: [{ required: true, message: '请输入中文名称' }],
              }
            ]"
          />
        </a-form-item>
        <a-form-item label='项目描述'>
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
    title: '项目ID',
    dataIndex: 'project_id'
  },
  {
    title: '项目名称',
    dataIndex: 'name'
  },
  {
    title: '中文名',
    dataIndex: 'cn_name'
  },
  {
    title: '状态',
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
  name: 'subject',
  components: {BfTable},
  data () {
    return {
      total:0,
      advanced: true,
      columns: columns,
      dataSource: [],
      selectedRows: [],
      visible:false,
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
    this.form = this.$form.createForm(this, { name: 'moduleList' });
    this.formDialog = this.$form.createForm(this, { name: 'formDialog' });
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
          this.params.name = fieldsValue["projectName"]
          this.params.begin_time = rangeValue?rangeValue[0].format("YYYY-MM-DD"):""
          this.params.end_time = rangeValue?rangeValue[1].format("YYYY-MM-DD"):""
          this.fetchData()
        });
    },
    fetchData(){
      API.ProjectList(this.params).then((res)=>{
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
    onShowEdit(record){
      this.visible = true
      this.isEdit = true
      this.$nextTick(()=>{
        this.formDialog.setFieldsValue({
          id:record.id,
          name:record.name,
          cnname:record.cn_name,
          description:record.description
        })
      })
    },
    onCreateSubject () {
      this.formDialog.validateFields((err, fieldsValue) => {
          if (err) {
            return;
          }
          let name = fieldsValue["name"],
              cn_name = fieldsValue["cnname"],
              description = fieldsValue["description"]||""
          let data = {
            name,
            cn_name,
            description
          }
          API.CreateSubject(data).then((res)=>{
            let result = res.data
            if(res.status == 200 && result.code == 0){
              this.$message.success("项目新增成功~")
              this.visible = false
              this.fetchData()
            }
            else{
              this.$message.error("项目新增失败:"+result.message)
            }
          })
        })
    },
    onUpdateSubject(){
      this.formDialog.validateFields((err, fieldsValue) => {
          if (err) {
            return;
          }
          let id = fieldsValue["id"],
              name = fieldsValue["name"],
              cn_name = fieldsValue["cnname"],
              description = fieldsValue["description"]||""
          let data = {
            id,
            name,
            cn_name,
            description
          }
          API.UpdateSubject(data).then((res)=>{
            let result = res.data
            if(res.status == 200){
              this.$message.success("项目更新成功~")
              this.onReset()
              this.fetchData()
            }
            else{
              this.$message.error("项目更新失败:"+result.message)
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
      API.DeleteSubject({id}).then((res)=>{
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

