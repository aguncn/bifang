<template>
  <a-layout-sider :class="['side-menu', 'beauty-scroll', 'shadow']" width="256px" :collapsible="collapsible" v-model="collapsed" :trigger="null">
    <div :class="['logo']">
      <router-link to="/dashboard">
        <img src="@/assets/logo.png">
        <h1>{{systemName}}</h1>
      </router-link>
    </div>
    <a-menu theme="dark" mode="inline" @select="onSelect"  :default-selected-keys="defaultKey" :open-keys.sync="openKey">
        <a-sub-menu v-for="menu in menuList" v-if="isVisible(menu.meta.role||[])" :key="menu.path">
          <span slot="title"><a-icon :type="menu.meta.icon||'form'" /><span>{{menu.name}}</span></span>
            <a-menu-item v-show="!(sub.meta&&(sub.meta.isShowMenu==false))" v-for="sub in menu.children" :key="sub.path">
              <router-link :to="menu.path+sub.path">{{sub.name}}</router-link>
            </a-menu-item>        
        </a-sub-menu>
    </a-menu>
  </a-layout-sider>
</template>

<script>
import {mapGetters} from 'vuex'
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
  computed:{
    ...mapGetters({
      'userRole':'getRoles'
    }),
  },
  created(){
    
     let match = this.$route.path.slice(1).split('/')
     if(match && match.length > 1){
        this.openKey = ["/"+match[0]]
        this.defaultKey = ["/"+match[1]]
     }
     let item = routeConfig.find(item=>item.path == '/')
     this.menuList = item?item.children:[]
     console.log('menu',this.menuList)
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
    isVisible(roleList){
      if(roleList.length == 0) return true;
      let isVisible = false
      console.log(roleList)
      this.userRole.forEach((item)=>{
        roleList.indexOf(item.id) > -1?isVisible=true:""
      })
      
      return isVisible
    },
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
