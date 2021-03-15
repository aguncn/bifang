import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const USER_KEY = "bifang.user"
const PERMISSIONS_KEY = "bifang.permission"
const ROLES_KEY = "bifang.roles"

export default new Vuex.Store({
  state: {
    user: null,
    permissions: null,
    roles: null,
  },
  getters:{
    getUser: state => {
      if (!state.user) {
        try {
          const user = localStorage.getItem(USER_KEY)
          state.user = JSON.parse(user)
        } catch (e) {
          console.error(e)
        }
      }
      return state.user
    },
    getPermissions: state => {
      if (!state.permissions) {
        try {
          const permissions = localStorage.getItem(PERMISSIONS_KEY)
          state.permissions = JSON.parse(permissions)
          state.permissions = state.permissions ? state.permissions : []
        } catch (e) {
          console.error(e.message)
        }
      }
      return state.permissions
    },
    getRoles: state => {
      if (!state.roles) {
        try {
          const roles = localStorage.getItem(ROLES_KEY)
          state.roles = JSON.parse(roles)
          state.roles = state.roles ? state.roles : []
        } catch (e) {
          console.error(e.message)
        }
      }
      return state.roles
    }
  },
  mutations: {
    setUser (state, user) {
      state.user = user
      localStorage.setItem(USER_KEY, JSON.stringify(user))
    },
    setPermissions(state, permissions) {
      state.permissions = permissions
      localStorage.setItem(PERMISSIONS_KEY, JSON.stringify(permissions))
    },
    setRoles(state, roles) {
      state.roles = roles
      localStorage.setItem(ROLES_KEY, JSON.stringify(roles))
    },
  }
})
