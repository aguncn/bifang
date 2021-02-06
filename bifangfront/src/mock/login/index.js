import Mock from 'mockjs'

Mock.mock(`${process.env.VUE_APP_API_BASE_URL}/jwt_auth/`, 'post', ({body}) => {

    return {
        "code": 0,
        "message": "欢迎回来",
        "data": {
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNjQyMzk3Njc2LCJlbWFpbCI6IiIsIm9yaWdfaWF0IjoxNjEwODYxNjc2fQ.hrxfF9plfuJgwc-5eP9n53KP2Rd8_ZqFkzAyoD76prA",
            "expireAt": "2022-01-17T05:34:36.588228",
            "user_id": 1,
            "user": {
                "id": 1,
                "name": "admin",
                "email": "",
                "avatar": ""
            },
            "is_superuser": true,
            "permissions": [
                {
                    "id": "queryForm",
                    "operation": [
                        "add",
                        "edit"
                    ]
                }
            ],
            "roles": [
                {
                    "id": "admin",
                    "operation": [
                        "add",
                        "edit",
                        "delete"
                    ]
                }
            ]
        }
    }
  
})



Mock.mock(`${process.env.VUE_APP_API_BASE_URL}/account/register`, 'post', ({body}) => {

    return {
        "code": 0,
        "message": "注册成功",
        "data": {'username': 'pkev1n', 'password': '123456', 'email': 'adbc@ad.com'}
    }
  
})