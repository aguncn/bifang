import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/antd.less'
import './theme/index.less'
import {request,initInterceptor} from '@/service/request'

Vue.config.productionTip = false;

Vue.use(Antd);
Vue.prototype.$request = request;
initInterceptor(Vue.prototype.$message)

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
