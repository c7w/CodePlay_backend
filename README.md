# Codeplay_backend

## Routing

### `/`

根目录，网站的主页。

### `/login`

登录中介页。

### `/api`

所有提供的 API 的入口。

## API

### `/api/userinfo`

[GET]

**Request params**

+ sessionId (从 cookies 中获取)
+ student_id (optimal, default = self.id)

**Response**

+ 首先对 sessionId 进行校验，如果未绑定用户，则返回 {"err": "not_logged_in"}
+ 如果用户是 User，则无视 student_id，返回自身的数据
+ 如果用户是 Designer，则返回 student_id 对应的数据。当没找到用户返回 {"err": "not_found"}
+ 否则返回查询到的用户数据，类似于

```json
{"student_id": 2020010951, "name": "cc7w", "fullname": "高焕昂", "email": "gha20@mails.tsinghua.edu.cn", "role": "User"}
```

[POST]

**Request body** (Content-Type: application/json)

+ sessionId
+ key (需要在 js 中先 MD5)

```json
{
  "student_id": 2020010951,
  "key": "339BD665D02F8C3E8DD262B59D67A904"
}
```

**Response**

+ 用于将用户提权至 Designer
+ 需要输入正确的口令 `CODEplayDESIGNER`
+ 输入正确则提权并返回用户信息，否则返回 {"status": "key verification failed"}

```json
{"student_id": 2020010951, "name": "cc7w", "fullname": "高焕昂", "email": "gha20@mails.tsinghua.edu.cn", "role": "Designer"}
```

### `/api/userScheme`

[GET]

**Request Params**

+ sessionId
+ student_id
+ sort_strategy: "submission_time", "vote", "hue"

**Response**

+ request_user: 当前用户
+ user: 被查询用户
+ 仅有设计师有权限查询别人的全部提交
+ schemes: 按照 sort_strategy 排序后的 schemes 的列表

[POST]

**Request Body**

+ operation: "create", "update", "vote", "delete", "approve", "disapprove"
+ sessionId (Only author could modify his or her own work, "approve" and "disapprove" only accessible to Designers)
+ id (Must provide if "update", "vote", "delete")
+ colors (Must fully provide if "create" or "update")
  + Presented in a list of lists, where each secondary list is [R,G,B,A,H,S,V]
+ name (Must provide if "create" or "update" )
+ description (Must provide if "create" or "update" )

+ author_id (must provide if "create". Ex. 2020010951)

+ sketch_id (must provide if "create". Ex. 1)

**Examples**

```json
{
  "sessionId": "sessionId",
  "operation": "create",
  "sketch_id": 1,
  "author_id": 2020010951,
  "name": "Runtime Error",
  "description": "Code Play GO GO GO",
  "colors":[
  	[0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1],
    [0.5,0.5,0.5,0.5,0.5,0.5,0.5]
  ]
}
```

```json
{
  "sessionId": "sessionId",
  "operation": "update",
  "id": 3,
  "name": "Runtime Errrrrrrrorrrrrrr",
  "description": "Code Play GO GOGOOGOGOGOGO",
  "colors":[
  	[0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1],
    [0.114514,0.5,0.5,0.5,0.5,0.5,0.5]
  ]
}
```

```json
{
  "sessionId": "sessionId",
  "operation": "vote",
  "id": 3
}
```

```json
{
  "sessionId": "sessionId",
  "operation": "delete",
  "id": 3
}
```

```json
{
  "sessionId": "sessionId",
  "operation": "approve",
  "id": 3
}
```

```json
{
  "sessionId": "sessionId",
  "operation": "disapprove",
  "id": 3
}
```

**Response**

注意这里 colors 为了存储方便，为 string 类型。

```
{
    "id":6,
    "submission_time":1633798831.651342,
    "sketch_id":1,
    "name":"Wrong Answer",
    "description":"Code Play GO GO GO",
    "likes":0,
    "approved":false,
    "author_id":2020010951,
    "hidden":false,
    "colors":"[[0, 0, 0, 0.2, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1], [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]]"
}
```

### `/api/exploreScheme`

[GET]

**Request Params**

+ sessionId
+ sketch_id
+ sort_strategy: "submission_time"(default), "vote", "hue", 'designer_name"
+ approved: (当提供本参数时 仅展示遴选后的结果)

**Response**

会根据玩家的权限，返回不同的排序后的 Scheme Model.

如果玩家是 User，只会返回随机一张，无视 sort_strategy 与 approved。

```json
{
    "schemes":[
        {
            "id":3,
            "submission_time":1633797634,
            "sketch_id":1,
            "name":"Runtime Errrrrrrrorrrrrrr",
            "description":"Code Play GO GOGOOGOGOGOGO",
            "likes":14,
            "approved":false,
            "author":{
                "student_id":2020010951,
                "name":"cc7w",
                "fullname":"高焕昂",
                "email":"gha20@mails.tsinghua.edu.cn",
                "role":"Designer"
            },
            "hidden":true,
            "colors":[
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0
                ],
                [
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1
                ],
                [
                    0.114514,
                    0.5,
                    0.5,
                    0.5,
                    0.5,
                    0.5,
                    0.5
                ]
            ]
        }
    ]
}
```

如果是 Designer，会返回所有 Scheme 的列表。

// 这里后续要不要加分页需求

```json
{
    "schemes":[
        {
            "id":3,
            "submission_time":1633797634,
            "sketch_id":1,
            "name":"Runtime Errrrrrrrorrrrrrr",
            "description":"Code Play GO GOGOOGOGOGOGO",
            "likes":14,
            "approved":false,
            "author":{
                "student_id":2020010951,
                "name":"cc7w",
                "fullname":"高焕昂",
                "email":"gha20@mails.tsinghua.edu.cn",
                "role":"Designer"
            },
            "hidden":true,
            "colors":[
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0
                ],
                [
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1
                ],
                [
                    0.114514,
                    0.5,
                    0.5,
                    0.5,
                    0.5,
                    0.5,
                    0.5
                ]
            ]
        },
        {
            "id":1,
            "submission_time":1633797654,
            "sketch_id":1,
            "name":"Runtime Error",
            "description":"Code Play GO GO GO",
            "likes":0,
            "approved":false,
            "author":{
                "student_id":2020010951,
                "name":"cc7w",
                "fullname":"高焕昂",
                "email":"gha20@mails.tsinghua.edu.cn",
                "role":"Designer"
            },
            "hidden":false,
            "colors":[
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0
                ],
                [
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1
                ],
                [
                    0.5,
                    0.5,
                    0.5,
                    0.5,
                    0.5,
                    0.5,
                    0.5
                ]
            ]
        },
        {
            "id":2,
            "submission_time":1633797644,
            "sketch_id":1,
            "name":"Runtime Error",
            "description":"Code Play GO GO GO",
            "likes":0,
            "approved":false,
            "author":{
                "student_id":2020010951,
                "name":"cc7w",
                "fullname":"高焕昂",
                "email":"gha20@mails.tsinghua.edu.cn",
                "role":"Designer"
            },
            "hidden":false,
            "colors":[
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0
                ],
                [
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1
                ],
                [
                    0.5,
                    0.5,
                    0.5,
                    0.5,
                    0.5,
                    0.5,
                    0.5
                ]
            ]
        },
        {
            "id":4,
            "submission_time":1633797624,
            "sketch_id":1,
            "name":"Runtime Error",
            "description":"Code Play GO GO GO",
            "likes":0,
            "approved":false,
            "author":{
                "student_id":2020010951,
                "name":"cc7w",
                "fullname":"高焕昂",
                "email":"gha20@mails.tsinghua.edu.cn",
                "role":"Designer"
            },
            "hidden":false,
            "colors":[
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0
                ],
                [
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1
                ],
                [
                    0.5,
                    0.5,
                    0.5,
                    0.5,
                    0.5,
                    0.5,
                    0.5
                ]
            ]
        },
        {
            "id":5,
            "submission_time":1633798717,
            "sketch_id":1,
            "name":"Accepted",
            "description":"Code Play GO GO GO",
            "likes":0,
            "approved":false,
            "author":{
                "student_id":2020010951,
                "name":"cc7w",
                "fullname":"高焕昂",
                "email":"gha20@mails.tsinghua.edu.cn",
                "role":"Designer"
            },
            "hidden":false,
            "colors":[
                [
                    0,
                    0,
                    0,
                    0.2,
                    0,
                    0,
                    0
                ],
                [
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1
                ],
                [
                    0.5,
                    0.5,
                    0.5,
                    0.5,
                    0.5,
                    0.5,
                    0.5
                ]
            ]
        },
        {
            "id":6,
            "submission_time":1633798831,
            "sketch_id":1,
            "name":"Wrong Answer",
            "description":"Code Play GO GO GO",
            "likes":0,
            "approved":false,
            "author":{
                "student_id":2020010951,
                "name":"cc7w",
                "fullname":"高焕昂",
                "email":"gha20@mails.tsinghua.edu.cn",
                "role":"Designer"
            },
            "hidden":false,
            "colors":[
                [
                    0,
                    0,
                    0,
                    0.2,
                    0,
                    0,
                    0
                ],
                [
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1
                ],
                [
                    0.5,
                    0.5,
                    0.5,
                    0.5,
                    0.5,
                    0.5,
                    0.5
                ]
            ]
        }
    ]
}
```

如果想对 scheme 修改请调用 `[POST] /api/userScheme`。

## Models

+ Scheme

```json
{
    "id": 114514,
    "submission_time": 1633747700,
    "name": "MyColorScheme",
    "author": {
        "student_id": 2020010951,
        "name": "cc7w",
        "fullname": "高焕昂",
        "role": "User"
    },
    "hidden": false,
    "colors": "[(R, G, B, A, H, S, V), (R, G, B, A, H, S, V)]"
}
```



## 与 Account9 的对接流程

### 应用信息

+ 客户端ID（Client ID）	8pKCWELExLFMkeqA4qZ8cpNItD0
+ 客户端密码（Client Secret）	shfKjrGJeS9EsYFlDHuQ

### Step. 1

Browser:
https://stu.cs.tsinghua.edu.cn/api/v2/authorize?response_type=code&client_id=8pKCWELExLFMkeqA4qZ8cpNItD0&redirect_uri=https://cc7w.cf

Redirect to:
http://cc7w.cf/?code=h2woy5nn4wv&state=you_should_specify_a_state

### Step. 2

[POST] https://stu.cs.tsinghua.edu.cn/api/v2/access_token

**Request Body**

```json
{
  "client_id": "8pKCWELExLFMkeqA4qZ8cpNItD0",
  "client_secret": "shfKjrGJeS9EsYFlDHuQ",
  "code": "qo6sfd1mzpr",
  "redirect_uri": "https://cc7w.cf"
}
```

**Response Body**

```json
{
    "access_token": "nk92jtejv6i",
    "refresh_token": "l2yj5l29wpf",
    "expires_in": 2591999
}
```

### Step. 3
[GET] https://stu.cs.tsinghua.edu.cn/api/v2/userinfo?access_token=nk92jtejv6i

**Response Body**

```json
{
    "err": null,
    "user":{
        "name": "cc7w",
        "fullname": "高焕昂",
        "student_id": "2020010951",
        "email": "gha20@mails.tsinghua.edu.cn",
        "student_type": "bachelor",
        "year": 2020,
        "class_number": 4,
        "mobile": "",
        "groups":[
        	"undergraduate20204"
        ]
    }
}
```
