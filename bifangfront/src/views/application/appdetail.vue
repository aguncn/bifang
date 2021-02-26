<template>
  <a-card :body-style="{padding: '24px 32px'}" :bordered="false">
    <a-form :form="form" @submit="isEdit?onUpdateApplication():onCreateApplication()">
      <a-form-item
          label="ID"
          v-show="false"
        >
          <a-input placeholder="自动生成" 
            v-decorator="['id']"
          />
        </a-form-item>
      <a-form-item 
        label='英文名称'
        :labelCol="{span: 7}"
        :wrapperCol="{span: 10}"
      >
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
      <a-form-item 
        label='中文名称'
        :labelCol="{span: 7}"
        :wrapperCol="{span: 10}">
        <a-input
        v-decorator="[
            'cn_name',
            {
            rules: [{ required: true, message: '请输入中文名称' }],
            }
        ]"
        />
      </a-form-item>
      <a-form-item
        label="归属项目"
        :labelCol="{span: 7}"
        :wrapperCol="{span: 10}"
      >
        <a-select
          show-search
          placeholder="请选择项目"
          option-filter-prop="children"
          style="width: 100%"
          :filter-option="filterOption"
          v-decorator="['project_id', { rules: [{ required: true, message: '请选择归属项目!' }] }]"
        >
          <a-select-option v-for="d in options" :key="d.value">
          {{ d.label }}
          </a-select-option>
        </a-select>
      </a-form-item>
      <a-form-item
        label="应用描述"
        :labelCol="{span: 7}"
        :wrapperCol="{span: 10}"
      >
        <a-textarea rows="4" 
        placeholder="请输入应用描述"
        v-decorator="['description']"
        />
      </a-form-item>
      <a-form-item
        label="GIT ID"
        :labelCol="{span: 7}"
        :wrapperCol="{span: 10}"
      >
        <a-input 
          placeholder="请输入git id"
          v-decorator="['git_id', { rules: [{ required: true, message: '请输入git id!' }] }]"
        />
      </a-form-item>
      <a-form-item
        label="GIT APPID"
        :labelCol="{span: 7}"
        :wrapperCol="{span: 10}"
      >
        <a-input 
          placeholder="请输入git appId"
          v-decorator="['git_app_id', { rules: [{ required: true, message: '请输入git appId!' }] }]"
        />
      </a-form-item>
      <a-form-item
        label="GIT Token"
        :labelCol="{span: 7}"
        :wrapperCol="{span: 10}"
      >
        <a-input 
          placeholder="请输入git token"
          v-decorator="['git_trigger_token', { rules: [{ required: true, message: '请输入git token!' }] }]"
        />
      </a-form-item>
      <a-form-item
        label="编译脚本"
        :labelCol="{span: 7}"
        :wrapperCol="{span: 10}"
      >
        <a-input 
          placeholder="请输入编译脚本路径"
          v-decorator="['build_script', { rules: [{ required: true, message: '请输入编译脚本路径!' }] }]"
        />
      </a-form-item>
      <a-form-item
        label="部署脚本"
        :labelCol="{span: 7}"
        :wrapperCol="{span: 10}"
      >
        <a-input 
          placeholder="请输入部署脚本路径"
          v-decorator="['deploy_script', { rules: [{ required: true, message: '请输入部署脚本路径!' }] }]"
        />
      </a-form-item>
      <a-form-item
        label="应用压缩包"
        :labelCol="{span: 7}"
        :wrapperCol="{span: 10}"
      >
        <a-input 
          placeholder="请输入应用压缩包路径"
          v-decorator="['zip_package_name', { rules: [{ required: true, message: '请输入应用压缩包路径!' }] }]"
        />
      </a-form-item>
      <a-form-item
        label="服务端口"
        :labelCol="{span: 7}"
        :wrapperCol="{span: 10}"
      >
        <a-input 
          placeholder="请输入服务端口"
          v-decorator="['service_port', { rules: [{ required: true, message: '请输入服务端口!' }] }]"
        />
      </a-form-item>
      <a-form-item
        label="执行用户"
        :labelCol="{span: 7}"
        :wrapperCol="{span: 10}"
      >
        <a-input 
          placeholder="请输入执行用户"
          v-decorator="['service_username', { rules: [{ required: true, message: '请输入执行用户!' }] }]"
        />
      </a-form-item>
      <a-form-item
        label="执行用户组"
        :labelCol="{span: 7}"
        :wrapperCol="{span: 10}"
      >
        <a-input 
          placeholder="请输入执行用户组"
          v-decorator="['service_group', { rules: [{ required: true, message: '请输入执行用户组!' }] }]"
        />
      </a-form-item>
      <a-form-item
        label="启停日志次数"
        :labelCol="{span: 7}"
        :wrapperCol="{span: 10}"
      >
        <a-input 
          placeholder="请输入启停日志次数"
          v-decorator="['op_log_no']"
        />
      </a-form-item>
      <a-form-item style="margin-top: 24px" :wrapperCol="{span: 10, offset: 7}">
        <a-button type="primary" html-type="submit">{{btnDesc}}</a-button>
      </a-form-item>
    </a-form>
  </a-card>
</template>

<script>
import API from '@/service'
export default {
  name: 'appDetail',
  data () {
    return {
      isEdit:false,
      value: 1,
      fetching:false,
      options:[],
      projectList:[],
      btnDesc:"创建"
    }
  },
  beforeCreate() {
    this.form = this.$form.createForm(this, { name: 'applicaitonDetail' });
  },
  created(){
    this.fetchProjectList()
    if(this.$route.params.id){
        this.isEdit=true
        this.btnDesc = "更新"
    }
    
  },
  mounted(){
    if(this.isEdit){
        this.$nextTick(()=>{
            this.form.setFieldsValue({
                ...this.$route.params,
                project_id: this.$route.params["project"],
                git_id: this.$route.params["git"]
            })
        })
    }
  },
  methods: {
    fetchProjectList(){
      API.ProjectList({}).then((res)=>{
        let result = res.data
        if(res.status == 200 && result.code == 0){
          this.projectList = result.data.results
          result.data.results.forEach(item=>{
            this.options.push({
              label:item.cn_name,
              value:item.id
            })
          })
        }
        else{
          this.$message,error("无法获取应用列表~")
        }
      })
    },
    onCreateApplication () {
      let self = this
      this.form.validateFields((err, fieldsValue) => {
          if (err) {
            return;
          }
          let project = self.projectList.find(item=>item.id == fieldsValue["project_id"])
          let data = {
            ...fieldsValue,
            project_name: project.name
          }
          API.CreateApplication(data).then((res)=>{
            let result = res.data
            if(res.status == 200 && result.code == 0){
              this.$message.success("应用创建成功~")
              this.$router.push("app")
            }
            else{
              this.$message.error("应用创建失败~:"+result.message)
            }
          })
        });
    },
    onUpdateApplication(){
      this.form.validateFields((err, fieldsValue) => {
          if (err) {
            return;
          }
          let project = this.options.find(item=>item.id == fieldsValue["project"])
          let data = {
            ...fieldsValue,
            project_name:project.name
          }
          API.UpdateApplication(data).then((res)=>{
            let result = res.data
            if(res.status == 200){
              this.$message.success("应用更新成功~")
            }
            else{
              this.$message.error("应用更新失败:"+result.message)
            }
          })
        })
    },
    filterOption(input, option) {
      return (
        option.componentOptions.children[0].text.toLowerCase().indexOf(input.toLowerCase()) >= 0
      );
    },
  }
}
</script>

<style scoped>

</style>
