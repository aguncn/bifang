import Vue from 'vue'
import VueRouter from 'vue-router'
// import MainLayout from '@/layouts/MainLayout.vue'
import {isLogin} from '@/utils/request'
import {routeConfig} from './config'
import {formatRoutes} from '@/utils/util'

Vue.use(VueRouter)

console.log('route config:',formatRoutes(routeConfig))

const routes = formatRoutes(routeConfig)

const router = new VueRouter({
  routes
})

/**
 * 增加登录路由拦截
 */
router.beforeEach((to, from, next) => {
  if (to.path === '/login') {
    next();
  } else {
    if (!isLogin()) {
      next('/login');
    } else {
      next();
    }
  }
});

export default router
