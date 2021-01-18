import Vue from 'vue'
import VueRouter from 'vue-router'
import MainLayout from '@/layouts/MainLayout.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: MainLayout,
    redirect: '/releaseList',
    children:[
      {
        path: 'releaseList',
        name: '发布单列表',
        meta: {
          icon: 'dashboard'
        },
        component: () => import('@/views/release/list')
      },
      {
        path: 'createRelease',
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

export default router
