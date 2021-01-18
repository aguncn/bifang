const path = require("path")
const isProd = process.env.NODE_ENV === 'production'

module.exports = {
    devServer: {
      // proxy: {
      //   '/api': { //此处要与 /services/api.js 中的 API_PROXY_PREFIX 值保持一致
      //     target: process.env.VUE_APP_API_BASE_URL,
      //     changeOrigin: true,
      //     pathRewrite: {
      //       '^/api': ''
      //     }
      //   }
      // }
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
    outputDir: 'dist',
    assetsDir: 'static',
    productionSourceMap: false
}