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
  computed: {
    // ...mapState('setting', ['layout', 'showPageTitle', 'pageWidth'])
    breadcrumb(){
      const list = ["首页"]
      if(this.$route.matched.length >1){
        list.push(this.$route.matched[1].meta.parent.name)
        list.push(this.$route.matched[1].name)
      }
      return list
    },
    title(){
      return this.$route.matched.length>1?(this.$route.matched[1].meta.title || this.$route.matched[1].name):"标题"
    }
  }
}
</script>

<style lang="less" scoped>
  @import "index";
</style>
