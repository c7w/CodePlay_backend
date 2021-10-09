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

+ student_id
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
+ 输入正确则提权并返回{"status": "ok"}，否则返回{"status": "failed"}

### `/api/userScheme`

[GET]

**Request Params**

+ sessionId
+ student_id
+ sort_strategy: "submission_time", "vote", "hue", 'designer_name"

**Response**

+ request_user: 当前用户
+ user: 被查询用户
+ 仅有设计师有权限查询别人的全部提交
+ schemes: 按照 sort_strategy 排序后的 schemes 的列表

[POST]

**Request Body**

+ operation: "create", "update", "vote", "delete"
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
  "operation": "vote",
  "id": 3
}
```

```json
{
  "operation": "delete",
  "id": 3
}
```

**Response**

```
{'id': 3, 'submission_time': datetime.datetime(2021, 10, 9, 18, 33, 51, 951358), 'sketch_id': 1, 'name': 'Runtime Errrrrrrrorrrrrrr', 'description': 'Code Play GO GOGOOGOGOGOGO', 'likes': 14, 'author_id': 2020010951, 'hidden': False, 'colors': '[[0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1], [0.114514, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]]'}
```



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

