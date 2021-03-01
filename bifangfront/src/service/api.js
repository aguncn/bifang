const BASE_URL = process.env.VUE_APP_API_BASE_URL;
const REAL_URL = process.env.VUE_APP_API_REAL_URL;
const API = {
    LOGIN: `${REAL_URL}/jwt_auth/`,
    REGISTER: `${REAL_URL}/account/register/`,
    RELEASELIST: `${REAL_URL}/release/list/`,
		RELEASEDETAIL: `${REAL_URL}/release/detail/`,
    RELEASEBUILD: `${REAL_URL}/release/build/`,
    RELEASEBUILDSTATUS: `${REAL_URL}/release/build_status/`,
    APPLICATIONLIST: `${REAL_URL}/app/list/`,
    ENVLIST: `${REAL_URL}/env/list/`,
    ENVEXCHANGE: `${REAL_URL}/env/exchange/`,
    SERVERLIST: `${REAL_URL}/server/list/`,
    PROJECTIST: `${REAL_URL}/project/list/`,
    CREATERELEASE: `${REAL_URL}/release/create/`,
    CREATESERVER:`${REAL_URL}/server/create/`,
    DELETESERVER: `${REAL_URL}/server/delete/{{id}}/`,
    UPDATESERVER: `${REAL_URL}/server/update/{{id}}/`,
    CREATESUBJECT: `${REAL_URL}/project/create/`,
    DELETESUBJECT: `${REAL_URL}/project/delete/{{id}}/`,
    UPDATESUBJECT: `${REAL_URL}/project/update/{{id}}/`,
    DELETEAPPLICATION: `${REAL_URL}/app/delete/{{id}}/`,
    CREATEAPPLICATION: `${REAL_URL}/app/create/`,
    UPDATEAPPLICATION: `${REAL_URL}/app/update/{{id}}/`,
    RELEASEHISTORY: `${REAL_URL}/history/release/`,
    SERVERHISTORY: `${REAL_URL}/history/server/`,
    GROUPLIST: `${REAL_URL}/account/groups/`,
    CREATEGROUP:`${REAL_URL}/account/groups/`,
    DELETEGROUP: `${REAL_URL}/account/groups/{{id}}/`,
    UPDATEGROUP: `${REAL_URL}/account/groups/{{id}}/`,
    USERLIST: `${REAL_URL}/account/users/`,
    CREATEUSER:`${REAL_URL}/account/users/`,
    DELETEUSER: `${REAL_URL}/account/users/{{id}}/`,
    UPDATEUSER: `${REAL_URL}/account/users/{{id}}/`,
}

export {
    API
}