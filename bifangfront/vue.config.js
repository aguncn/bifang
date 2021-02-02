const path = require("path")
const isProd = process.env.NODE_ENV === 'production'

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