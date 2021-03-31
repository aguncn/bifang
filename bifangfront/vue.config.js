const path = require("path")
const isProd = process.env.NODE_ENV === 'production'

const assetsCDN = {
  // webpack build externals
  externals: {
    vue: 'Vue',
    'vue-router': 'VueRouter',
    vuex: 'Vuex',
    axios: 'axios',
    '@antv/data-set': 'DataSet',
    'js-cookie': 'Cookies'
  },
  css: [
  ],
  js: [
    '//cdn.jsdelivr.net/npm/vue@2.6.11/dist/vue.min.js',
    '//cdn.jsdelivr.net/npm/vue-router@3.3.4/dist/vue-router.min.js',
    '//cdn.jsdelivr.net/npm/vuex@3.4.0/dist/vuex.min.js',
    '//cdn.jsdelivr.net/npm/axios@0.19.2/dist/axios.min.js',
    '//cdn.jsdelivr.net/npm/nprogress@0.2.0/nprogress.min.js',
    '//cdn.jsdelivr.net/npm/clipboard@2.0.6/dist/clipboard.min.js',
    '//cdn.jsdelivr.net/npm/@antv/data-set@0.11.4/build/data-set.min.js',
    '//cdn.jsdelivr.net/npm/js-cookie@2.2.1/src/js.cookie.min.js'
  ]
}

module.exports = {
    devServer: {
      proxy: {
        '/restapi': { //此处要与 /services/api.js 中的 API_PROXY_PREFIX 值保持一致
          target: 'http://127.0.0.1:8000',
          changeOrigin: true,
          pathRewrite: {
            '^/restapi': '/'
          }
        }
      }
    },
    pluginOptions: {
        'style-resources-loader': {
            preProcessor: 'less',
            patterns: [path.resolve(__dirname, "./src/theme/index.less")],
        }
    },
    chainWebpack: (config)=>{
      //修改文件引入自定义路径
      config.resolve.alias
          .set('@', path.resolve(__dirname, "src"))
      // 生产环境下使用CDN
      if (isProd) {
        config.plugin('html')
          .tap(args => {
            args[0].cdn = assetsCDN
          return args
        })
      }
    },
    css: {
      loaderOptions: {
        less: {
          lessOptions: {
            modifyVars: {
              'primary-color': '#1DA57A',
              'link-color': '#1DA57A',
              'border-radius-base': '2px'
            },
            javascriptEnabled: true
          }
        }
      }
    },
    publicPath: isProd ? '/bifang/' : '/',
    outputDir: 'build',
    assetsDir: 'static',
    productionSourceMap: false
}