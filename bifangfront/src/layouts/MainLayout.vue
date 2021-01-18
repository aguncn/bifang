<template>
  <a-layout :class="['admin-layout', 'beauty-scroll']">
    <side-menu :class="['fixed-side']" :collapsed="collapsed" :collapsible="true" />
    <div :style="`width: ${sideMenuWidth}; min-width: ${sideMenuWidth};max-width: ${sideMenuWidth};`" class="virtual-side"></div>
    <a-layout class="admin-layout-main beauty-scroll">
      <admin-header :style="headerStyle" :collapsed="collapsed" @toggleCollapse="toggleCollapse"/>
      <a-layout-content class="admin-layout-content" :style="`min-height: ${minHeight}px;`">
        <div style="position: relative">
          <page-view title="标题" :breadcrumb="breadcrumb"></page-view>
        </div>
      </a-layout-content>
      <a-layout-footer style="padding: 0px">
        <page-footer />
      </a-layout-footer>
    </a-layout>
  </a-layout>
</template>

<script>
import AdminHeader from '@/components/header/header'
import PageFooter from '@/components/footer/footer'
import SideMenu from '@/components/menu/sideMenu'
import PageView from './pageView/PageView'
// import {mapState, mapMutations, mapGetters} from 'vuex'

// const minHeight = window.innerHeight - 64 - 122

export default {
  name: 'MainLayout',
  components: { AdminHeader, SideMenu, PageFooter, PageView},
  data () {
    return {
      minHeight: window.innerHeight - 64 - 122,
      breadcrumb:["首页","二级","菜单"],
      collapsed: false
    }
  },
  provide() {
    return {
      adminLayout: this
    }
  },
  watch: {
    // $route(val) {
    //   this.setActivated(val)
    // },
    // layout() {
    //   this.setActivated(this.$route)
    // }
  },
  computed: {
    // ...mapState('setting', ['isMobile', 'theme', 'layout', 'footerLinks', 'copyright', 'fixedHeader', 'fixedSideBar',
    //   'fixedTabs', 'hideSetting', 'multiPage']),
    // ...mapGetters('setting', ['firstMenu', 'subMenu', 'menuData']),
    sideMenuWidth() {
      return this.collapsed ? '80px' : '256px'
    },
    headerStyle() {
    //   let width =  `calc(100% - ${this.sideMenuWidth})`
      return `width: 100%; position:static`
    },
    headMenuData() {
      const {layout, menuData, firstMenu} = this
      return layout === 'mix' ? firstMenu : menuData
    },
    sideMenuData() {
      const {layout, menuData, subMenu} = this
      return layout === 'mix' ? subMenu : menuData
    }
  },
  methods: {
    // ...mapMutations('setting', ['correctPageMinHeight', 'setActivatedFirst']),
    toggleCollapse () {
      this.collapsed = !this.collapsed
    },
    onMenuSelect () {
      this.toggleCollapse()
    }
  },
  created() {
    //this.correctPageMinHeight(this.minHeight - 24)
    //this.setActivated(this.$route)
  },
  beforeDestroy() {
    // this.correctPageMinHeight(-this.minHeight + 24)
  }
}
</script>

<style lang="less" scoped>
  .admin-layout{
    .side-menu{
      &.fixed-side{
        position: fixed;
        height: 100vh;
        left: 0;
        top: 0;
      }
    }
    .virtual-side{
      transition: all 0.2s;
    }
    .virtual-header{
      transition: all 0.2s;
      opacity: 0;
      &.fixed-tabs.multi-page:not(.fixed-header){
        height: 0;
      }
    }
    .admin-layout-main{
      .admin-header{
        top: 0;
        right: 0;
        overflow: hidden;
        transition: all 0.2s;
        &.fixed-tabs.multi-page:not(.fixed-header){
          height: 0;
        }
      }
    }
    .admin-layout-content{
      padding: 24px 24px 0;
      /*overflow-x: hidden;*/
      /*min-height: calc(100vh - 64px - 122px);*/
    }
  }
</style>
