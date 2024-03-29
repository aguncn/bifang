const BASE_URL = process.env.VUE_APP_API_BASE_URL;
const REAL_URL = process.env.VUE_APP_API_REAL_URL;
const API = {
    LOGIN: `${REAL_URL}/jwt_auth/`,
    REGISTER: `${REAL_URL}/account/register/`,
    RELEASELIST: `${REAL_URL}/release/list/`,
    CREATERELEASE: `${REAL_URL}/release/create/`,
		RELEASEDETAIL: `${REAL_URL}/release/detail/`,
    RELEASEBUILD: `${REAL_URL}/release/build/`,
    RELEASEBUILDSTATUS: `${REAL_URL}/release/build_status/`,
    APPLICATIONLIST: `${REAL_URL}/app/list/`,
    ENVLIST: `${REAL_URL}/env/list/`,
    ENVEXCHANGE: `${REAL_URL}/env/exchange/`,
    DEPLOY: `${REAL_URL}/deploy/deploy/`,
    GITLIST: `${REAL_URL}/gitapp/list/`,
    SERVERLIST: `${REAL_URL}/server/list/`,
    CREATESERVER:`${REAL_URL}/server/create/`,
    DELETESERVER: `${REAL_URL}/server/delete/{{id}}/`,
    UPDATESERVER: `${REAL_URL}/server/update/{{id}}/`,
    PROJECTLIST: `${REAL_URL}/project/list/`,
    CREATEPROJECT: `${REAL_URL}/project/create/`,
    DELETEPROJECT: `${REAL_URL}/project/delete/{{id}}/`,
    UPDATEPROJECT: `${REAL_URL}/project/update/{{id}}/`,
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
    PERMISSIONLIST: `${REAL_URL}/permission/list/`,
    CREATEPERMISSION: `${REAL_URL}/permission/create/`,
    DELETEPERMISSION: `${REAL_URL}/permission/delete/{{id}}/`,
    ALLCOUNT: `${REAL_URL}/stats/all_count/`,
    RELEASETOP5: `${REAL_URL}/stats/release_top5/`,
    RELEASEFAILEDTOP5: `${REAL_URL}/stats/release_failed_top5/`
}

export {
    API
}