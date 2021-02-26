<template>
  <a-layout-sider :class="['side-menu', 'beauty-scroll', 'shadow']" width="256px" :collapsible="collapsible" v-model="collapsed" :trigger="null">
    <div :class="['logo']">
      <router-link to="/dashboard">
        <img src="@/assets/logo.png">
        <h1>{{systemName}}</h1>
      </router-link>
    </div>
    <a-menu theme="dark" mode="inline" @select="onSelect"  :default-selected-keys="defaultKey" :open-keys.sync="openKey">
        <a-sub-menu v-for="menu in menuList" :key="menu.path">
          <span slot="title"><a-icon :type="menu.meta.icon||'form'" /><span>{{menu.name}}</span></span>
            <a-menu-item v-for="sub in menu.children" :key="sub.path">
              <router-link :to="menu.path+sub.path">{{sub.name}}</router-link>
            </a-menu-item>        
        </a-sub-menu> 
        <!--<a-sub-menu key="/release">
          <span slot="title"><a-icon type="profile" /><span>发布单</span></span>
          <a-menu-item key="/releaseList">
            <router-link to="/release/releaseList">列表</router-link>
          </a-menu-item>
          <a-menu-item key="/createRelease">
            <router-link to="/release/createRelease">新建</router-link>
          </a-menu-item>
        </a-sub-menu>
        <a-sub-menu key="sub2">
          <span slot="title"><a-icon type="apartment" /><span>环境</span></span>
          <a-menu-item key="3">
            <router-link to="/transfer">流转</router-link>
          </a-menu-item>
          <a-menu-item key="4">
            <router-link to="/envlist">列表</router-link>
          </a-menu-item>
        </a-sub-menu>
        <a-sub-menu key="sub3">
          <span slot="title"><a-icon type="cloud-upload" /><span>部署</span></span>
          <a-menu-item key="5">
            <router-link to="/deploy">服务部署</router-link>
          </a-menu-item>
          <a-menu-item key="6">
            <router-link to="/startup">服务启停</router-link>
          </a-menu-item>
        </a-sub-menu>
        <a-sub-menu key="sub4">
          <span slot="title"><a-icon type="appstore" /><span>项目应用</span></span>
          <a-menu-item key="7">
            <router-link to="/subject">项目</router-link>
          </a-menu-item>
          <a-menu-item key="8">
            <router-link to="/application">应用</router-link>
          </a-menu-item>
        </a-sub-menu>
        <a-sub-menu key="sub5">
          <span slot="title"><a-icon type="cluster" /><span>服务器</span></span>
          <a-menu-item key="9">
            <router-link to="/serverlist">列表</router-link>
          </a-menu-item>
          <a-menu-item key="10">
            <router-link to="/addserver">新增</router-link>
          </a-menu-item> 
        </a-sub-menu>
        <a-sub-menu key="sub6">
          <span slot="title"><a-icon type="appstore" /><span>账户</span></span>
          <a-menu-item key="10">
            <router-link to="/group">用户组</router-link>
          </a-menu-item>
          <a-menu-item key="11">
            <router-link to="/user">用户</router-link>
          </a-menu-item>
        </a-sub-menu>-->
    </a-menu>
  </a-layout-sider>
</template>

<script>
// import {mapState} from 'vuex'
import {routeConfig} from '@/router/config'
export default {
  name: 'SideMenu',
  data(){
    return {
      systemName:"毕方部署平台",
      menuList:[],
      defaultKey:['/createRelease'],
      openKey:['/release']
    }
  },
  created(){
    
     let match = this.$route.path.slice(1).split('/')
     if(match && match.length > 1){
        this.openKey = ["/"+match[0]]
        this.defaultKey = ["/"+match[1]]
     }
     let item = routeConfig.find(item=>item.path == '/')
     this.menuList = item?item.children:[]
     console.log('route',this.openKey,this.defaultKey)
  },
  props: {
    collapsible: {
      type: Boolean,
      required: false,
      default: false
    },
    collapsed: {
      type: Boolean,
      required: false,
      default: false
    },
    // todo--动态生成菜单
    // menuData: {
    //   type: Array,
    //   required: true
    // }
  },
  methods: {
    onSelect (obj) {
      console.log("select",obj)
      this.$emit('menuSelect', obj)
    }
  }
}
</script>

<style lang="less" scoped>
@import "index";
</style>
