
<template>
  <a-card>
    <div class="search">
      <a-form layout="horizontal" :form="form">
        <div class="fold">
          <a-row >
          <a-col :md="8" :sm="24" >
            <a-form-item
              label="组件"
              :labelCol="{span: 5}"
              :wrapperCol="{span: 18, offset: 1}"
            >
              <a-input name="" placeholder="请输入" />
            </a-form-item>
          </a-col>
          <a-col :md="8" :sm="24" >
            <a-form-item
              label="组件"
              :labelCol="{span: 5}"
              :wrapperCol="{span: 18, offset: 1}"
            >
              <a-select placeholder="请选择">
                <a-select-option value="1">关闭</a-select-option>
                <a-select-option value="2">运行中</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :md="8" :sm="24" >
            <a-form-item
              label="组件状态"
              :labelCol="{span: 7}"
              :wrapperCol="{span: 16,offset: 1}"
            >
              <a-input placeholder="请输入" />
            </a-form-item>
          </a-col>
        </a-row>
        </div>
        <span style="float: right; margin-top: 3px;">
          <a-button type="primary">查询</a-button>
          <a-button style="margin-left: 8px">重置</a-button>
        </span>
      </a-form>
    </div>
    <div>
      <bf-table
        :columns="columns"
        :dataSource="dataSource"
        :selectedRows.sync="selectedRows"
        @clear="onClear"
        @change="onChange"
        @selectedRowChange="onSelectChange"
        :pagination="{
          current: page,
          pageSize: pageSize,
          total: total,
          showSizeChanger: true,
          showLessItems: true,
          showQuickJumper: true,
          showTotal: (total, range) => `第 ${range[0]}-${range[1]} 条，总计 ${total} 条`,
          onChange: onPageChange,
          onShowSizeChange: onSizeChange,
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
    sorter: true
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
      page:1,
      pageSize:20,
      total:0,
      advanced: true,
      columns: columns,
      dataSource: [],
      selectedRows: []
    }
  },
  created(){
    this.query()
  },
  methods: {
    deleteRecord(key) {
      this.dataSource = this.dataSource.filter(item => item.key !== key)
      this.selectedRows = this.selectedRows.filter(item => item.key !== key)
    },
    toggleAdvanced () {
      this.advanced = !this.advanced
    },
    remove () {
      this.dataSource = this.dataSource.filter(item => this.selectedRows.findIndex(row => row.key === item.key) === -1)
      this.selectedRows = []
    },
    query(){
      let params = {
        currentPage:this.page,
        pageSize:this.pageSize
      }
      ReleaseList().then((res)=>{
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
    onPageChange(){
      this.page = page
      this.pageSize = pageSize
      this.query()
    },
    onSizeChange(current, size) {
      this.page = 1
      this.pageSize = size
      this.query()
    },
    onClear() {
      this.$message.info('您清空了勾选的所有行')
    },
    onStatusTitleClick() {
      this.$message.info('你点击了状态栏表头')
    },
    onChange() {
      this.$message.info('表格状态改变了')
    },
    onSelectChange() {
      this.$message.info('选中行改变了')
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

