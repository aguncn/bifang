<template>
  <div class="common-layout">
    <div class="content"><slot></slot></div>
    <page-footer></page-footer>
  </div>
</template>

<script>
import PageFooter from '@/components/footer/footer'
import {mapState} from 'vuex'

export default {
  name: 'CommonLayout',
  components: {PageFooter}
}
</script>

<style scoped lang="less">
.common-layout{
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: auto;
  background-color: @layout-body-background;
  background-image: url('https://gw.alipayobjects.com/zos/rmsportal/TVYTbAXWheQpRcWDaDMu.svg');
  background-repeat: no-repeat;
  background-position-x: center;
  background-position-y: 110px;
  background-size: 100%;
  .content{
    padding: 32px 0;
    flex: 1;
    @media (min-width: 768px){

      padding: 112px 0 24px;
    }
  }
}
</style>
