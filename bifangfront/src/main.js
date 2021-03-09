import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import Antd from 'ant-design-vue'
import echarts from 'echarts'
import 'ant-design-vue/dist/antd.less'
import './theme/index.less'
import '@/mock'
import {request,initInterceptor} from '@/utils/request'

Vue.config.productionTip = false;

Vue.use(Antd);
Vue.prototype.$request = request;
Vue.prototype.$echarts = echarts;
initInterceptor(Vue.prototype.$message,router)

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
