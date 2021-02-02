<template>
  <common-layout>
    <div class="top">
      <div class="header">
        <img alt="logo" class="logo" src="@/assets/logo.png" />
        <span class="title">毕方部署平台</span>
      </div>
      <div class="desc">BiFang 是最具影响力的服务部署平台</div>
    </div>
    <div class="login">
      
        <a-tabs size="large" :activeKey="activeKey" @change="onTabChange" :tabBarStyle="{textAlign: 'center'}" style="padding: 0 2px;">
          <a-tab-pane tab="登录" key="1">
            <a-form @submit="onLogin" :form="loginForm">
                <a-alert type="error" :closable="true" v-show="error" :message="error" showIcon style="margin-bottom: 24px;" />
                <a-form-item>
                <a-input
                    autocomplete="autocomplete"
                    size="large"
                    placeholder="admin"
                    v-decorator="['name', {rules: [{ required: true, message: '请输入账户名', whitespace: true}]}]"
                >
                    <a-icon slot="prefix" type="user" />
                </a-input>
                </a-form-item>
                <a-form-item>
                <a-input
                    size="large"
                    placeholder="888888"
                    autocomplete="autocomplete"
                    type="password"
                    v-decorator="['password', {rules: [{ required: true, message: '请输入密码', whitespace: true}]}]"
                >
                    <a-icon slot="prefix" type="lock" />
                </a-input>
                </a-form-item>
                <div>
                <a-checkbox :checked="true" >自动登录</a-checkbox>
                    <a style="float: right">忘记密码</a>
                </div>
                <a-button :loading="logging" style="width: 100%;margin-top: 24px" size="large" htmlType="submit" type="primary">登录</a-button>
            </a-form>
          </a-tab-pane>
          <a-tab-pane tab="注册" key="2">
            <a-form @submit="onRegister" :form="registerForm">
                <a-alert type="error" :closable="true" v-show="regError" :message="regError" showIcon style="margin-bottom: 24px;" />
                <a-form-item>
                <a-input
                    autocomplete="autocomplete"
                    size="large"
                    placeholder="请输入用户名"
                    v-decorator="['username', {rules: [{ required: true, message: '请输入账户名', whitespace: true}]}]"
                >
                    <a-icon slot="prefix" type="user" />
                </a-input>
                </a-form-item>
                <a-form-item>
                <a-input
                    size="large"
                    placeholder="请输入密码"
                    autocomplete="autocomplete"
                    type="password"
                    v-decorator="['password', {rules: [{ required: true, message: '请输入密码', whitespace: true}]}]"
                >
                    <a-icon slot="prefix" type="lock" />
                </a-input>
                </a-form-item>
                <a-form-item>
                <a-input
                    size="large"
                    placeholder="请输入确认密码"
                    autocomplete="autocomplete"
                    type="password"
                    v-decorator="['confirmPassword', { rules: [{ required: true, message: '请输入确认密码!'}, { validator: compareToPassword}] }]"
                >
                    <a-icon slot="prefix" type="lock" />
                </a-input>
                </a-form-item>
                <a-form-item>
                    <a-input 
                    size="large" 
                    placeholder="请输入邮箱"
                    type="email"
                    v-decorator="['email',{rules: [{ type: 'email',message: '输入的邮箱地址不正确！'},{ required: true,message: '请输入邮箱'}]}]">
                        <a-icon slot="prefix" type="mail" />
                    </a-input>
                </a-form-item>
                <a-form-item>
                    <a-button :loading="registing" style="width: 100%;margin-top: 24px" size="large" htmlType="submit" type="primary">注册</a-button>
                </a-form-item>
            </a-form>
          </a-tab-pane>
        </a-tabs>
        <div>
        </div>
    </div>
  </common-layout>
</template>

<script>
import CommonLayout from '@/layouts/CommonLayout'
import {Login,Register} from '@/service'
import {setAuthorization} from '@/utils/request'
// import {mapMutations} from 'vuex'

export default {
  name: 'Login',
  components: {CommonLayout},
  data () {
    return {
      logging: false,
      registing:false,
      error: '',
      regError:'',
      activeKey:'1',
      loginForm: this.$form.createForm(this),
      registerForm: this.$form.createForm(this)
    }
  },
  methods: {
    // ...mapMutations('account', ['setUser', 'setPermissions', 'setRoles']),
    onLogin (e) {
      e.preventDefault()
      this.loginForm.validateFields((err) => {
        if (!err) {
          this.logging = true
          const username = this.loginForm.getFieldValue('name')
          const password = this.loginForm.getFieldValue('password')
          Login({username, password}).then(this.afterLogin)
        }
      })
    },
    onRegister (e) {
      e.preventDefault()
      this.registerForm.validateFields((err) => {
        if (!err) {
          this.registing = true
          const username = this.registerForm.getFieldValue('username')
          const password = this.registerForm.getFieldValue('password')
          const passwordConfirm = this.registerForm.getFieldValue('confirmPassword')
          const email = this.registerForm.getFieldValue('email')
          Register({username, password, passwordConfirm, email}).then(this.afterRegister)
        }
      })
    },
    compareToPassword(rule, value, callback) {
      const form = this.registerForm;
      if (value && value !== form.getFieldValue('password')) {
        callback('两次输入的密码不同');
      } else {
        callback();
      }
    },
    onTabChange(key){
        this.activeKey = key
    },
    setUser(user){

    },
    afterLogin(res) {
      this.logging = false
      const loginRes = res.data
      if (loginRes.code == 0) {
        const {user, permissions, roles} = loginRes.data
        this.setUser(user)
        // this.setPermissions(permissions)
        // this.setRoles(roles)
        setAuthorization({token: loginRes.data.token, expireAt: new Date(loginRes.data.expireAt)})
        this.$router.push('/releaseList')
        // 获取路由配置
        // getRoutesConfig().then(result => {
        //   const routesConfig = result.data.data
        //   loadRoutes(routesConfig)
        //   this.$router.push('/dashboard/workplace')
        //   this.$message.success(loginRes.message, 3)
        // })
      } else {
        this.error = loginRes.data.message
      }
    },
    afterRegister(res) {
      const registerRes = res.data
      this.registing = false;
      if (registerRes.code == 0) {
        this.$message.success('恭喜，注册成功！', 3)
        const username = this.registerForm.getFieldValue('username')
        const password = this.registerForm.getFieldValue('password')
        this.registerForm.resetFields()
        //回填
        this.loginForm.setFieldsValue({
            name:username,
            password
            })
        this.activeKey = "1"
      } else {
        this.regError =registerRes.data
      }
    }
  }
}
</script>

<style lang="less" scoped>
  .common-layout{
    .top {
      text-align: center;
      .header {
        height: 44px;
        line-height: 44px;
        a {
          text-decoration: none;
        }
        .logo {
          height: 44px;
          vertical-align: top;
          margin-right: 16px;
        }
        .title {
          font-size: 33px;
          color: @bf-title-color;
          font-family: 'Myriad Pro', 'Helvetica Neue', Arial, Helvetica, sans-serif;
          font-weight: 600;
          position: relative;
          top: 2px;
        }
      }
      .desc {
        font-size: 14px;
        color: @bf-text-color-second;
        margin-top: 12px;
        margin-bottom: 40px;
      }
    }
    .login{
      width: 368px;
      margin: 0 auto;
      @media screen and (max-width: 576px) {
        width: 95%;
      }
      @media screen and (max-width: 320px) {
        .captcha-button{
          font-size: 14px;
        }
      }
      .icon {
        font-size: 24px;
        color: @bf-text-color-second;
        margin-left: 16px;
        vertical-align: middle;
        cursor: pointer;
        transition: color 0.3s;

        &:hover {
          color: @bf-primary-color;
        }
      }
    }
  }
</style>
