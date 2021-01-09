// https://eslint.org/docs/user-guide/configuring

module.exports = {
  'parser': "vue-eslint-parser",
  'parserOptions': {
    'parser': 'babel-eslint',
    'ecmaVersion': 2018,
    'sourceType': 'module'
  },

  // add your custom rules here
  'rules': {
    'no-tabs': 0,
    'no-mixed-spaces-and-tabs': 0,
    'indent': ["off", "tab"],
    'no-trailing-spaces': 0
  }
}