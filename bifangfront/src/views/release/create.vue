<template>
  <a-card :body-style="{padding: '24px 32px'}" :bordered="false">
    <a-form :form="form" @submit="submitHandler">
      <a-form-item
        label="发布单号"
        :labelCol="{span: 7}"
        :wrapperCol="{span: 10}"
      >
        <a-input disabled value="自动生成" placeholder="自动生成" />
      </a-form-item>
      <a-form-item
        label="组件选择"
        :labelCol="{span: 7}"
        :wrapperCol="{span: 10}"
      >
        <a-select
          show-search
          placeholder="请选择组件"
          option-filter-prop="children"
          style="width: 200px"
          :filter-option="filterOption"
          @focus="handleFocus"
          @blur="handleBlur"
          @change="handleChange"
          v-decorator="['appId', { rules: [{ required: true, message: '请选择发布的组件!' }] }]"
        >
          <a-select-option v-for="d in options" :key="d.value">
          {{ d.label }}
          </a-select-option>
        </a-select>
      </a-form-item>
      <a-form-item
        label="发布分支"
        :labelCol="{span: 7}"
        :wrapperCol="{span: 10}"
      >
        <a-input 
          placeholder="请输入发布单分支"
          v-decorator="['branch', { rules: [{ required: true, message: '请输入组件分支!' }] }]"
        />
      </a-form-item>
      <a-form-item
        label="发布描述"
        :labelCol="{span: 7}"
        :wrapperCol="{span: 10}"
      >
        <a-textarea rows="4" 
        placeholder="请输入发布单描述"
        v-decorator="['description', { rules: [{ required: false, message: '请输入组件分支!' }] }]"
        />
      </a-form-item>
      <a-form-item style="margin-top: 24px" :wrapperCol="{span: 10, offset: 7}">
        <a-button type="primary" html-type="submit">创建</a-button>
      </a-form-item>
    </a-form>
  </a-card>
</template>

<script>
import API from '@/service'
console.log("API",API)
export default {
  name: 'createRelease',
  data () {
    return {
      value: 1,
      fetching:false,
      options:[]
    }
  },
  beforeCreate() {
    this.form = this.$form.createForm(this, { name: 'createRelease' });
  },
  created(){
    this.fetch()
  },
  computed: {
    desc() {
    }
  },
  methods: {
    fetch(){
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
          this.$message,error("无法获取应用列表~")
        }
      })
    },
    handleChange(value) {
      console.log(`selected ${value}`);
    },
    handleBlur() {
      console.log('blur');
    },
    handleFocus() {
      console.log('focus');
    },
    submitHandler(e){
      e.preventDefault()
      this.form.validateFields((err, fieldsValue) => {
          if (err) {
            return;
          }
          let data = {
            name:"",
            app_id:fieldsValue["appId"],
            git_branch:fieldsValue["branch"],
            description:fieldsValue["description"]
          }
          API.CreateRelease(data).then((res)=>{
            let result = res.data
            if(res.status == 200 && result.code == 0){
              this.$message.success("发布单创建成功~")
              this.$router.push("releaseList")
            }
            else{
              this.$message.error("无法获取应用列表~")
            }
          })
        });
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
