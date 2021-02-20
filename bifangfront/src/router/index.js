import Vue from 'vue'
import VueRouter from 'vue-router'
import MainLayout from '@/layouts/MainLayout.vue'
import {isLogin} from '@/utils/request'

Vue.use(VueRouter)

const routes = [
  {
    path: '/login',
    name: '登录页',
    component: () => import('@/views/login/login')
  },
  {
    path: '/',
    name: 'Home',
    component: MainLayout,
    redirect: '/releaseList',
    children:[
      {
        path: '/release/releaseList',
        name: '发布单列表',
        meta: {
          icon: 'dashboard'
        },
        component: () => import('@/views/release/list')
      },
      {
        path: '/release/createRelease',
        name: '新建发布单',
        meta: {
          icon: 'dashboard'
        },
        component: () => import('@/views/release/create')
      },
      {
        path: 'transfer',
        name: '流转列表',
        meta: {
          icon: 'dashboard'
        },
        component: () => import('@/views/environment/transfer')
      },
      {
        path: 'history',
        name: '历史记录',
        meta: {
          icon: 'dashboard'
        },
        component: () => import('@/views/environment/history')
      },
      {
        path: 'envlist',
        name: '环境列表',
        meta: {
          icon: 'dashboard'
        },
        component: () => import('@/views/environment/envlist')
      },
      {
        path: 'deploy',
        name: '服务部署',
        meta: {
          icon: 'dashboard'
        },
        component: () => import('@/views/deployment/deploy')
      },
      {
        path: 'startup',
        name: '服务启停',
        meta: {
          icon: 'dashboard'
        },
        component: () => import('@/views/deployment/startup')
      },
      {
        path: 'subject',
        name: '项目',
        meta: {
          icon: 'dashboard'
        },
        component: () => import('@/views/application/subject')
      },
      {
        path: 'application',
        name: '组件',
        meta: {
          icon: 'dashboard'
        },
        component: () => import('@/views/application/app')
      },
      {
        path: '/appdetail',
        name: 'appdetail',
        meta: {
          icon: 'dashboard'
        },
        component: () => import('@/views/application/appdetail')
      },
      {
        path: '/serverlist',
        name: '服务器列表',
        meta: {
          icon: 'dashboard'
        },
        component: () => import('@/views/server/list')
      },
      {
        path: '/group',
        name: '账户组列表',
        meta: {
          icon: 'dashboard'
        },
        component: () => import('@/views/account/group')
      },
      {
        path: '/user',
        name: '用户列表',
        meta: {
          icon: 'dashboard'
        },
        component: () => import('@/views/account/user')
      },
    ]
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  }
]

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
