import { requestWhitelistConfig } from '@/utils/request'
import account from './account'
import application from './application'
import env from './environment'
import git from './git'
import release from './release'
import deploy from './deploy'
import server from './server'
import history from './history'
import permission from './permission'
import {API} from './api'

requestWhitelistConfig([
    API.LOGIN,
    API.REGISTER
])

export default {
    ...account,
    ...application,
    ...env,
    ...git,
    ...release,
    ...deploy,
    ...server,
    ...history,
    ...permission
}