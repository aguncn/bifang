<template>
  <div class="page-layout">
    <div :class="['page-header', layout]">
      <div class="page-header-wide">
        <div class="breadcrumb">
          <a-breadcrumb>
            <a-breadcrumb-item :key="index" v-for="(item, index) in breadcrumb">
              <span>{{item}}</span>
            </a-breadcrumb-item>
          </a-breadcrumb>
        </div>
        <div class="detail">
          <div class="main">
            <div class="row">
              <h1 class="title">{{title}}</h1>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div ref="page" :class="['page-content', layout]" >
      <router-view ref="page" />
    </div>
  </div>
</template>

<script>
// import {mapState} from 'vuex'
export default {
  name: 'PageHeader',
  data(){
      return {
          layout:'side'
      }
  },
  props: {
    title: {
      type: [String, Boolean],
      required: false
    },
    breadcrumb: {
      type: Array,
      required: false
    }
  },
  computed: {
    // ...mapState('setting', ['layout', 'showPageTitle', 'pageWidth'])
  }
}
</script>

<style lang="less" scoped>
  @import "index";
</style>
