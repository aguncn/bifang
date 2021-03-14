<template>
  <a-layout-header :class="['light', 'admin-header']">
    <div :class="['admin-header-wide']">
      <a-icon class="trigger" :type="collapsed ? 'menu-unfold' : 'menu-fold'" @click="toggleCollapse"/>

      <div :class="['admin-header-right', 'dark']">
          <a-tooltip class="header-item" title="帮助文档" placement="bottom" >
            <a href="https://iczer.gitee.io/vue-antd-admin-docs/" target="_blank">
              <a-icon type="question-circle-o" />
            </a>
          </a-tooltip>
          <a-dropdown>
            <div class="header-avatar" style="cursor: pointer">
                <a-avatar class="avatar" size="small" shape="circle" :src="avatar"/>
                <span class="name">{{user.name}}</span>
            </div>
            <a-menu :class="['avatar-menu']" slot="overlay">
            <!-- <a-menu-item>
                <a-icon type="user" />
                <span>个人中心</span>
            </a-menu-item> 
            <a-menu-divider />-->
            <a-menu-item @click="logout">
                <a-icon style="margin-right: 8px;" type="poweroff" />
                <span>退出登录</span>
            </a-menu-item>
            </a-menu>
        </a-dropdown>
      </div>
    </div>
  </a-layout-header>
</template>

<script>
import {mapState,mapGetters} from 'vuex'
import {logout} from '@/utils/request'

export default {
  name: 'AdminHeader',
  props: ['collapsed'],
  data() {
    return {
      avatar: 'https://gw.alipayobjects.com/zos/rmsportal/gaOngJwsRYRaVAuXXcmB.png',
      searchActive: false
    }
  },
  computed: {
    ...mapGetters({
      'user':'getUser'
    }),
  },
  methods: {
    toggleCollapse () {
      this.$emit('toggleCollapse')
    },
    logout() {
      logout()
      this.$router.push('/login')
    }
  }
}
</script>

<style lang="less" scoped>
@import "index";
</style>
