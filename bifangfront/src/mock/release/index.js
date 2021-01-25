import Mock from 'mockjs'

const releaseList = Mock.mock({
  'list|100': [{
    'key|+1': 0,
    'no': 'NO-@integer(1,100)',
    'description': `组件-@integer(1,100)`,
    'callNo': `@integer(1,100)`,
    'status|1-4': 1,
    'updatedAt': '@DATETIME'
  }]
})

Mock.mock(RegExp(`${process.env.VUE_APP_API_BASE_URL}/release/list`),'get', ({url}) => {
  const params = {}
  let {page, pageSize} = params
  page = eval(page) - 1 || 0
  pageSize = eval(pageSize) || 10
  delete params.page
  delete params.pageSize
  let result = releaseList.list.filter(item => {
    for (let [key, value] of Object.entries(params)) {
      if (item[key] != value) {
        return false
      }
    }
    return true
  })
  const total = result.length
  if ((page) * pageSize > total) {
    result = []
  } else {
    result = result.slice(page * pageSize, (page + 1) * pageSize)
  }
  return {
    code: 0,
    message: 'success',
    results: {
      page: page + 1,
      pageSize,
      total,
      list: result
    }
  }
})