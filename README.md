# Codeplay_backend

## Deploy

修改前端的内容，特别是 Settings.tsx，**注意地址不要加最后的slash `/`**

使用yarn build 或者 npx react-scripts build

后端删掉templates 里面的 index.html ， static 里面的 css js 文件夹

把build 里面的 index.html, ./static/css, ./static/js 放到刚刚删掉的位置

修改后端的 Backend/settings.py 里面的服务器地址，**注意不要加最后的slash `/`**



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
  "key": "339bd665d02f8c3e8dd262b59d67a904"
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

### `/api/sketch`

[GET]

**Request Params**

None

**Response**

示例返回：

```json
{
    "sketch_list":[
        {
            "id": 1,
            "name": "balloon",
            "colors": 6,
            "data": "<svg t=\"1633693832542\" class=\"icon\" viewBox=\"0 0 1024 1024\" version=\"1.1\" xmlns=\"http://www.w3.org/2000/svg\" p-id=\"1470\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" width=\"200\" height=\"200\">\r\n    <defs>\r\n        <style type=\"text/css\"></style>\r\n    </defs>\r\n    <path d=\"M413.5 629.7c-1.1-6.2-7.1-10.3-13.1-9.1-6.2 1.1-10.3 7-9.1 13.1l47.6 262.8c0.9 4.7 4.5 8.2 9 9.1 1.4 0.2 2.8 0.3 4.2 0 6.2-1.1 10.3-7 9.1-13.1l-47.7-262.8zM563.1 892.5c-1.1 6.2 3 12.1 9.1 13.1 1.4 0.2 2.8 0.2 4.2 0 4.5-0.9 8.1-4.4 9-9.1L633 633.8c1.1-6.2-3-12.1-9.1-13.1-6.2-1.1-12.1 3-13.1 9.1l-47.7 262.7z\" %%1%% p-id=\"1471\"></path>\r\n    <path d=\"M598.4 982H425.7c-23.3 0-42.3-18.9-42.3-42.3v-79.9c0-16.7 13.5-30.1 30.1-30.1h196.9c16.7 0 30.1 13.5 30.1 30.1v79.9c0.2 23.4-18.7 42.3-42.1 42.3z\" %%2%% p-id=\"1472\"></path>\r\n    <path d=\"M523.4 919.1v-27h40.5c6.3 0 11.3-5 11.3-11.3 0-5.1-3.3-9.4-8-10.8-1.1-0.3-2.2-0.5-3.3-0.5h-40.5v-39.7h-22.6v39.7H459v-39.7h-22.6v39.7h-52.6v22.6h52.6V982H459v-40.3h181.7v-22.6H523.4z m-22.7 0H459v-27h41.8l-0.1 27z\" %%3%% p-id=\"1473\"></path>\r\n    <path d=\"M797.3 417.9c-15.1 54-45.1 101.8-85.3 138.6-40.2 36.7-63.1 88.7-63.1 143 0 5.3-2.1 10.1-5.6 13.5-3.5 3.5-8.2 5.6-13.5 5.6H394.2c-5.2 0-10-2.1-13.6-5.6-3.4-3.4-5.7-8.2-5.7-13.6 0-54.4-22.8-106.2-62.8-142.8-40.3-36.9-70.4-84.7-85.5-138.8h187.6c-3.2-27.8-4.9-57.4-4.9-88.1 0-37.1 2.5-72.6 7.1-105.1H238.5C283.3 117.5 389.4 42 512.1 42h4.5c121.5 1.8 225.1 76.7 269.1 182.6h-178c4.6 32.6 7.1 68 7.1 105.1 0 30.7-1.7 60.3-4.9 88.1l187.4 0.1z\" %%4%% p-id=\"1474\"></path>\r\n    <path d=\"M614.7 329.8c0 30.7-1.7 60.3-4.9 88.1-6 52.5-17.3 98.4-32.1 133-16.2 38-25.1 78.7-25.1 120.1v47.7h-81.2V671c0-41.3-8.9-82.1-25.1-120.1-14.7-34.5-26-80.5-32-133-3.2-27.8-4.9-57.4-4.9-88.1 0-37.1 2.5-72.6 7.1-105.1C431.4 117.7 468.6 42 512.1 42c28.4 0 54 32.2 72.6 84.3 9.9 27.8 17.8 61.2 23 98.4 4.5 32.5 7 68 7 105.1z\" %%1%% p-id=\"1475\"></path>\r\n    <path d=\"M808.2 338.1c0 27.6-3.8 54.4-10.9 79.8H226.7c-7.2-25.9-11-53.2-10.9-81.4 0.2-39.6 8.3-77.4 22.7-111.8h547.1c14.6 34.9 22.6 73.2 22.6 113.4z\" %%5%% p-id=\"1476\"></path>\r\n    <path d=\"M614.7 329.8c0 30.7-1.7 60.3-4.9 88.1H414.3c-3.2-27.8-4.9-57.4-4.9-88.1 0-37.1 2.5-72.6 7.1-105.1h191.2c4.5 32.5 7 68 7 105.1z\" %%6%% p-id=\"1477\"></path>\r\n</svg>",
            "hidden": null,
            "defaultValue": "[[\"#2F9B77\", 1],[\"#F2B843\", 1],[\"#EA800C\", 1],[\"#3DC38A\", 1],[\"#F2B843\", 1],[\"#EA800C\", 1]]"
        }
    ]
}
```





## Models

### Scheme

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

### Sketch

正确的 svg 文件类型是下面这个样子。我们要做的不是更改 Point 的位置，而是在合适的位置加入 `fill="#2F9B77" fill-opacity="0.5"` 这种字符串。

```xml
<svg t="1633693832542" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1470" xmlns:xlink="http://www.w3.org/1999/xlink" width="200" height="200">
    <defs>
        <style type="text/css"></style>
    </defs>
    <path d="M413.5 629.7c-1.1-6.2-7.1-10.3-13.1-9.1-6.2 1.1-10.3 7-9.1 13.1l47.6 262.8c0.9 4.7 4.5 8.2 9 9.1 1.4 0.2 2.8 0.3 4.2 0 6.2-1.1 10.3-7 9.1-13.1l-47.7-262.8zM563.1 892.5c-1.1 6.2 3 12.1 9.1 13.1 1.4 0.2 2.8 0.2 4.2 0 4.5-0.9 8.1-4.4 9-9.1L633 633.8c1.1-6.2-3-12.1-9.1-13.1-6.2-1.1-12.1 3-13.1 9.1l-47.7 262.7z" fill="#2F9B77" fill-opacity="0.5" p-id="1471"></path>
    <path d="M598.4 982H425.7c-23.3 0-42.3-18.9-42.3-42.3v-79.9c0-16.7 13.5-30.1 30.1-30.1h196.9c16.7 0 30.1 13.5 30.1 30.1v79.9c0.2 23.4-18.7 42.3-42.1 42.3z" fill="#F2B843" p-id="1472"></path>
    <path d="M523.4 919.1v-27h40.5c6.3 0 11.3-5 11.3-11.3 0-5.1-3.3-9.4-8-10.8-1.1-0.3-2.2-0.5-3.3-0.5h-40.5v-39.7h-22.6v39.7H459v-39.7h-22.6v39.7h-52.6v22.6h52.6V982H459v-40.3h181.7v-22.6H523.4z m-22.7 0H459v-27h41.8l-0.1 27z" fill="#EA800C" p-id="1473"></path>
    <path d="M797.3 417.9c-15.1 54-45.1 101.8-85.3 138.6-40.2 36.7-63.1 88.7-63.1 143 0 5.3-2.1 10.1-5.6 13.5-3.5 3.5-8.2 5.6-13.5 5.6H394.2c-5.2 0-10-2.1-13.6-5.6-3.4-3.4-5.7-8.2-5.7-13.6 0-54.4-22.8-106.2-62.8-142.8-40.3-36.9-70.4-84.7-85.5-138.8h187.6c-3.2-27.8-4.9-57.4-4.9-88.1 0-37.1 2.5-72.6 7.1-105.1H238.5C283.3 117.5 389.4 42 512.1 42h4.5c121.5 1.8 225.1 76.7 269.1 182.6h-178c4.6 32.6 7.1 68 7.1 105.1 0 30.7-1.7 60.3-4.9 88.1l187.4 0.1z" fill="#3DC38A" p-id="1474"></path>
    <path d="M614.7 329.8c0 30.7-1.7 60.3-4.9 88.1-6 52.5-17.3 98.4-32.1 133-16.2 38-25.1 78.7-25.1 120.1v47.7h-81.2V671c0-41.3-8.9-82.1-25.1-120.1-14.7-34.5-26-80.5-32-133-3.2-27.8-4.9-57.4-4.9-88.1 0-37.1 2.5-72.6 7.1-105.1C431.4 117.7 468.6 42 512.1 42c28.4 0 54 32.2 72.6 84.3 9.9 27.8 17.8 61.2 23 98.4 4.5 32.5 7 68 7 105.1z" fill="#2F9B77" p-id="1475"></path>
    <path d="M808.2 338.1c0 27.6-3.8 54.4-10.9 79.8H226.7c-7.2-25.9-11-53.2-10.9-81.4 0.2-39.6 8.3-77.4 22.7-111.8h547.1c14.6 34.9 22.6 73.2 22.6 113.4z" fill="#F2B843" p-id="1476"></path>
    <path d="M614.7 329.8c0 30.7-1.7 60.3-4.9 88.1H414.3c-3.2-27.8-4.9-57.4-4.9-88.1 0-37.1 2.5-72.6 7.1-105.1h191.2c4.5 32.5 7 68 7 105.1z" fill="#EA800C" p-id="1477"></path>
</svg>
```

通过 [GET] /api/sketch 拿到的 sketch 列表的 sketch 字符串如下：

```xml
<svg t="1633693832542" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1470" xmlns:xlink="http://www.w3.org/1999/xlink" width="200" height="200">
    <defs>
        <style type="text/css"></style>
    </defs>
    <path d="M413.5 629.7c-1.1-6.2-7.1-10.3-13.1-9.1-6.2 1.1-10.3 7-9.1 13.1l47.6 262.8c0.9 4.7 4.5 8.2 9 9.1 1.4 0.2 2.8 0.3 4.2 0 6.2-1.1 10.3-7 9.1-13.1l-47.7-262.8zM563.1 892.5c-1.1 6.2 3 12.1 9.1 13.1 1.4 0.2 2.8 0.2 4.2 0 4.5-0.9 8.1-4.4 9-9.1L633 633.8c1.1-6.2-3-12.1-9.1-13.1-6.2-1.1-12.1 3-13.1 9.1l-47.7 262.7z" %%1%% p-id="1471"></path>
    <path d="M598.4 982H425.7c-23.3 0-42.3-18.9-42.3-42.3v-79.9c0-16.7 13.5-30.1 30.1-30.1h196.9c16.7 0 30.1 13.5 30.1 30.1v79.9c0.2 23.4-18.7 42.3-42.1 42.3z" %%2%% p-id="1472"></path>
    <path d="M523.4 919.1v-27h40.5c6.3 0 11.3-5 11.3-11.3 0-5.1-3.3-9.4-8-10.8-1.1-0.3-2.2-0.5-3.3-0.5h-40.5v-39.7h-22.6v39.7H459v-39.7h-22.6v39.7h-52.6v22.6h52.6V982H459v-40.3h181.7v-22.6H523.4z m-22.7 0H459v-27h41.8l-0.1 27z" %%3%% p-id="1473"></path>
    <path d="M797.3 417.9c-15.1 54-45.1 101.8-85.3 138.6-40.2 36.7-63.1 88.7-63.1 143 0 5.3-2.1 10.1-5.6 13.5-3.5 3.5-8.2 5.6-13.5 5.6H394.2c-5.2 0-10-2.1-13.6-5.6-3.4-3.4-5.7-8.2-5.7-13.6 0-54.4-22.8-106.2-62.8-142.8-40.3-36.9-70.4-84.7-85.5-138.8h187.6c-3.2-27.8-4.9-57.4-4.9-88.1 0-37.1 2.5-72.6 7.1-105.1H238.5C283.3 117.5 389.4 42 512.1 42h4.5c121.5 1.8 225.1 76.7 269.1 182.6h-178c4.6 32.6 7.1 68 7.1 105.1 0 30.7-1.7 60.3-4.9 88.1l187.4 0.1z" %%4%% p-id="1474"></path>
    <path d="M614.7 329.8c0 30.7-1.7 60.3-4.9 88.1-6 52.5-17.3 98.4-32.1 133-16.2 38-25.1 78.7-25.1 120.1v47.7h-81.2V671c0-41.3-8.9-82.1-25.1-120.1-14.7-34.5-26-80.5-32-133-3.2-27.8-4.9-57.4-4.9-88.1 0-37.1 2.5-72.6 7.1-105.1C431.4 117.7 468.6 42 512.1 42c28.4 0 54 32.2 72.6 84.3 9.9 27.8 17.8 61.2 23 98.4 4.5 32.5 7 68 7 105.1z" %%1%% p-id="1475"></path>
    <path d="M808.2 338.1c0 27.6-3.8 54.4-10.9 79.8H226.7c-7.2-25.9-11-53.2-10.9-81.4 0.2-39.6 8.3-77.4 22.7-111.8h547.1c14.6 34.9 22.6 73.2 22.6 113.4z" %%5%% p-id="1476"></path>
    <path d="M614.7 329.8c0 30.7-1.7 60.3-4.9 88.1H414.3c-3.2-27.8-4.9-57.4-4.9-88.1 0-37.1 2.5-72.6 7.1-105.1h191.2c4.5 32.5 7 68 7 105.1z" %%6%% p-id="1477"></path>
</svg>
```

我们前端工程师要做的事 是将 %%i%% replace 成为 `fill="#2F9B77" fill-opacity="0.5"` 这种字符串。

之后添加新线稿就这样强行写进去。

![image-20211010172133472](https://i.loli.net/2021/10/10/sbeB8YIqjChu7xi.png)

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
