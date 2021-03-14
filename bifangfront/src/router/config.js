import MainLayout from '@/layouts/MainLayout.vue'
const routeConfig = [
    {
      path: '/login',
      name: '登录页',
      component: () => import('@/views/login/login')
    },
    {
      path: '/',
      name: 'Home',
      component: MainLayout,
      redirect: '/dashboard/workspace',
      children:[
        {
          path: '/dashboard',
          name: 'Dashboard',
          meta:{
            icon: 'dashboard'
          },
          children:[
            {
              path: '/workspace',
              name: '工作台',
              meta:{
                title: "工作台"
              },
              component: () => import('@/views/dashboard/workspace')
            }
          ]
        },
        {
            path: '/release',
            name: '发布单',
            meta: {
              icon: 'profile'
            },
            children:[
              {
                  path: '/releaseList',
                  name: '列表',
                  meta:{
                    title: "发布单列表"
                  },
                  component: () => import('@/views/release/list')
              },
              {
                  path: '/createRelease',
                  name: '新建',
                  component: () => import('@/views/release/create')
              },
              {
                path: '/releaseHistory',
                name: '发布单部署历史',
                meta:{
                  isShowMenu:false
                },
                component: () => import('@/views/release/history')
              },
            ]
        },
        {
            path: '/environment',
            name: '环境',
            meta: {
              icon: 'apartment'
            },
            children:[
                {
                    path: '/environmentList',
                    name: '流转环境',
                    component: () => import('@/views/environment/envlist')
                  }
            ]
        },
        {
            path: '/deployment',
            name: '部署',
            meta: {
              icon: 'cloud-upload'
            },
            children:[
                {
                    path: '/deployList',
                    name: '服务部署',
                    component: () => import('@/views/deployment/deployList')
                },
                {
                  path: '/deploy',
                  name: '发布单部署',
                  meta:{
                    isShowMenu:false
                  },
                  component: () => import('@/views/deployment/deploy')
                }
            ]
        },
        {
            path: '/application',
            name: '项目应用',
            meta: {
              icon: 'appstore'
            },
            children:[
                {
                    path: '/project',
                    name: '项目',
                    component: () => import('@/views/application/project')
                  },
                  {
                    path: '/app',
                    name: '应用',
                    component: () => import('@/views/application/app')
                  },
                  {
                    path: '/appDetail',
                    name: '应用详情',
                    meta: {
                      isShowMenu: false
                    },
                    component: () => import('@/views/application/appdetail')
                  },
            ]
        },
        {
            path: '/server',
            name: '服务器',
            meta: {
              icon: 'cluster'
            },
            children:[
                {
                    path: '/serverlist',
                    name: '列表',
                    component: () => import('@/views/server/list')
                },
                {
                  path: '/serverHistory',
                  name: '服务器操作历史',
                  meta: {
                    isShowMenu: false
                  },
                  component: () => import('@/views/server/history')
              },
            ]
        },
        {
            path: '/account',
            name: '账户',
            meta: {
              icon: 'appstore'
            },
            children:[
                {
                    path: '/group',
                    name: '账户组',
                    component: () => import('@/views/account/group')
                },
                {
                    path: '/user',
                    name: '用户',
                    component: () => import('@/views/account/user')
                },
            ]
        }
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

export {
    routeConfig
}