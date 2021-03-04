import { requestWhitelistConfig } from '@/utils/request'
import account from './account'
import application from './application'
import env from './environment'
import release from './release'
import deploy from './deploy'
import server from './server'
import {API} from './api'

requestWhitelistConfig([
    API.LOGIN,
    API.REGISTER
])

export default {
    ...account,
    ...application,
    ...env,
    ...release,
    ...deploy,
    ...server
}