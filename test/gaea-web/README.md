# gaea-live

盖亚-直播，主要实现视频直播、点播， 用户聊天互动，页面组建设计等基础数据模型和页面组件（名称来源于next.baidu.com 系列页面设计工具）

# 数据模型

数据模型使用`GraphQL`定义，后端使用`graphql-php`实现


> [GraphQL](https://github.com/facebook/graphql) GraphQL is a query language and execution engine tied to any backend service. [doc](http://facebook.github.io/graphql/)

> [graphql-php](https://github.com/webonyx/graphql-php) A PHP port of GraphQL reference implementation [doc](http://webonyx.github.io/graphql-php/)

基本数据模型定义文件位于`phpsrc/GraphQL`目录下 对应命名空间`namespace Gaea\GraphQL;` [gitlab](http://gitlab.aodianyun.com/g1/gaea-live/tree/master/phpsrc/GraphQL)

安装php依赖

``` shell
composer update
```

## 根查询定义 [AbstractQueryType.php](http://gitlab.aodianyun.com/g1/gaea-live/blob/master/phpsrc/GraphQL/AbstractQueryType.php)

```php
<?php

namespace Gaea\GraphQL;


use GraphQL\Type\Definition\ObjectType;
use GraphQL\Type\Definition\ResolveInfo;

abstract class AbstractQueryType extends ObjectType
{
    public static $sync_room_topic = 'sync_room';
    public static $sync_user_topic = 'sync_user';
    public static $sync_lss_topic = 'sys/notify/lss';
    public static $present_user_topic = '__present__';

    /* $_config 可以添加其他的查询字段， $type 使用自己的类型注册 */
    public function __construct(array $_config = [], $type = null)
    {
        if (is_null($type)) {
            $type = new Types();
        }
        /* $config['fields'] 定义了允许的根查询类型 */
        $config = [
            'name' => 'Query',
            'fields' => [
                'user' => [
                    'type' => $type::BasicUser(),
                    'description' => 'Returns user by id',
                    'args' => [
                        'user_id' => $type::nonNull($type::id())
                    ]
                ],
                'deprecatedField' => [
                    'type' => $type::string(),
                    'deprecationReason' => 'This field is deprecated!'
                ],
                'fieldWithException' => [
                    'type' => $type::string(),
                    'resolve' => function () {
                        throw new \Exception("Exception message thrown in field resolver");
                    }
                ],
                'hello' => $type::string()
            ],
            'resolveField' => function ($val, $args, $context, ResolveInfo $info) {
                return $this->{$info->fieldName}($val, $args, $context, $info);
            }
        ];
        parent::__construct($config);
    }

    /* 获取数据 虚方法 需要具体实现 */
    abstract public function user($rootValue, $args, $context, ResolveInfo $info);

    /* 同步数据 虚方法 需要具体实现 */
    abstract public function sync_user($user_id, $dms_s_key);

    abstract public function sync_room($room_id, $dms_s_key);

    /* 测试字段 */
    public function hello()
    {
        return 'Your graphql-php endpoint is ready! Use GraphiQL to browse API';
    }

    public function deprecatedField()
    {
        return 'You can request deprecated field, but it is not displayed in auto-generated documentation by default.';
    }

}
```

## 类型注册 [Types.php](http://gitlab.aodianyun.com/g1/gaea-live/blob/master/phpsrc/GraphQL/Types.php)

```php
<?php
namespace Gaea\GraphQL;


use Gaea\GraphQL\ExtType\CurrentUser;
use Gaea\GraphQL\Union\MsgContentUnion;
use Gaea\GraphQL\Union\PlayerConfigUnion;

class Types extends BaseTypes
{
    /* 每一个公开方法 相当于一个类型的单实例实现  防止类型构造多次 */
    private static $_mPlayerConfigUnion = null;

    /**
     * @return PlayerConfigUnion
     */
    public static function PlayerConfigUnion()
    {
        return self::$_mPlayerConfigUnion ?: (self::$_mPlayerConfigUnion = new PlayerConfigUnion());
    }
    
}
```

## 可扩展的类型 [AbstractBasicRoom.php](http://gitlab.aodianyun.com/g1/gaea-live/blob/master/phpsrc/GraphQL/AbstractBasicRoom.php)

```php
<?php
/**
 * Created by PhpStorm.
 * User: Administrator
 * Date: 2017/4/25 0025
 * Time: 15:54
 */

namespace Gaea\GraphQL;


use Gaea\GraphQL\Type\BasicRoom;
use GraphQL\Type\Definition\ResolveInfo;

abstract class AbstractBasicRoom extends BasicRoom
{

    public function __construct(array $_config = [], $type = null)
    {
        if (is_null($type)) {
            /** @var Types $type */
            $type = new Types();
        }
        $config = [];

        /* 增加字段 播放器配置 */
        $config = [];
        $config['fields']['playerConfig'] = [
            'type' => $type::PlayerConfigUnion(),
            'description' => '播放器配置',
            'args' => [
                'player_type' => $type::nonNull($type::string())
            ]
        ];

        if (!empty($_config['fields'])) {
            $config['fields'] = array_merge($config['fields'], $_config['fields']);
        }
        parent::__construct($config, $type);
    }

    /* 虚方法 获取 播放器配置 $rootValue 为房间基本数据 即 BasicRoom, $args 为字段描述中的参数 $args['player_type']， $context 为查询上下文  即下文中 GraphQLApi 实例 */
    abstract public function playerConfig($rootValue, $args, $context, ResolveInfo $info);
}
```

# DEMO 

demo后端接口定义文件位于`gaeademo/api`目录下 对应命名空间`namespace gaeademo\api;` [gitlab](http://gitlab.aodianyun.com/g1/gaea-live/tree/master/gaeademo/api)


## GraphQL查询入口 [GraphQLApi.php](http://gitlab.aodianyun.com/g1/gaea-live/blob/master/gaeademo/api/GraphQLApi.php)

POST到接口 `/api/GraphQLApi/exec` 参数 `query` 查询语句，`variables` 查询绑定变量

```php<?php
/**
 * Created by PhpStorm.
 * User: Administrator
 * Date: 2017/3/12 0012
 * Time: 17:08
 */

namespace gaeademo\api;

use gaeademo\api\GraphQL\Types;
use ErrorException;
use gaeademo\common\ApiContext;

use \GraphQL\Schema;
use \GraphQL\GraphQL;
use \GraphQL\Type\Definition\Config;
use \GraphQL\Error\FormattedError;

class GraphQLApi extends ApiContext
{

    public function exec($query = '{hello}', array $variables = null)
    {
        if (DEV_MODEL == 'DEBUG') {
            Config::enableValidation(); 
            $phpErrors = []; 
            set_error_handler(function ($severity, $message, $file, $line) use (&$phpErrors) {
                $phpErrors[] = new ErrorException($message, 0, $severity, $file, $line);
            });
        }
        try {
            $schema = new Schema([
                'query' => Types::query()
            ]);
            /* $this 为上下文信息  可在查询中获取当前上下文信息 检查权限 */
            $result = GraphQL::execute(
                $schema,
                $query,
                null,
                $this,
                $variables
            );
            if (DEV_MODEL == 'DEBUG' && !empty($phpErrors)) {
                $result['extensions']['phpErrors'] = array_map(['GraphQL\Error\FormattedError', 'createFromPHPError'], $phpErrors);
            }
        } catch (\Exception $error) {
            $result['extensions']['exception'] = FormattedError::createFromException($error);
        }

        return $result;
    }

}
```

## 类型实现 [gaeademo/api/GraphQL](http://gitlab.aodianyun.com/g1/gaea-live/tree/master/gaeademo/api/GraphQL)

继承并实现 GraphQL 中的数据模型  实现类型注册

## 接口测试 [GraphiQL](http://gitlab.aodianyun.com/g1/gaea-live/tree/master/gaeademo/static/GraphiQL)

[接口测试](http://gaea.app/static/GraphiQL/)


``` gql
{
  hello,
  user(user_id:1001){
    user_id,
    nick,
    avatar
  }
}
```

``` gql
{
	room(room_id: 101){
    room_id
    room_title
    room_status
    currentUser{
      user{
        user_id
        nick
        avatar
        user_type
      }
    }
    playerConfig(player_type: "mpsplayer"){
      ... on PlayerMpsConfig{
        appId,
        autostart,
        controlbardisplay,
        isclickplay,
        isfullscreen,
        mobilefullscreen,
        player_type,
        room_id,
        stretching,
        uin,
      }
      ... on PlayerAodianConfig{
        adveDeAddr,
        autostart,
        bufferlength,
        controlbardisplay,
        defvolume,
        hlsUrl,
        maxbufferlength,
        player_type,
        room_id,
        rtmpUrl,
        stretching,
      }
    }
  }
}
```

# 测试数据

测试数据 位于 `db-migrate` 目录下 [gitlab](http://gitlab.aodianyun.com/g1/gaea-live/tree/master/db-migrate)

使用 `Flask-SQLAlchemy` 和 `SQLAlchemy-migrate` 管理数据库部署

> 文档 [Flask 中的数据库](http://www.pythondoc.com/flask-mega-tutorial/database.html#id4)

## 创建数据库
``` shell
python db_create.py
```

## 增加数据库版本
``` shell
python db_migrate.py
```

## 数据库升级
``` shell
python db_upgrade.py
```

## 测试数据导入
``` shell
python db_seed.py
```

# 前端页面 原生js

原生js位于 `gaeademo/static` 目录下 [gitlab](http://gitlab.aodianyun.com/g1/gaea-live/tree/master/gaeademo/static)

手机版页面 [demo_mobile.html](http://gaea.app/static/demo_mobile.html?room_id=101)

PC版页面 [demo.html](http://gaea.app/static/demo.html?room_id=101)


# 前端页面 vue组件

原生js位于 `websrc` 目录下 [gitlab](http://gitlab.aodianyun.com/g1/gaea-live/tree/master/websrc)

安装js依赖

``` shell
npm install cnpm -g
cnpm install webpack -g
cnpm install
```

打包文件
``` shell
webpack -w
```

vue手机版页面 [index.html](http://gaea.page/?room_id=101)


# 登录用户测试 

开发者后台 [develop](http://gaea.app/index.php?m=develop&c=index&a=index)

输入 ` 'DEVELOP_KEY' => 'TinyWebDev' ` 进入开发者环境


API测试 [selectapi](http://gaea.app/index.php?m=develop&c=syslog&a=selectapi)

选择 `TestApi.getUser`接口 输入 user_id 1000 - 1009 获取用户token
``` javascript
{
    "user": {
        "user_id": 1001,
        "nick": "Nick1001",
        "avatar": "http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png",
        "user_type": "authorized"
    },
    "token": "Ah_BRlsZIBbA55axnKWfu0uNwFrtF3ADI8KHM"
}
```

把token参数附加到预览页面之后即可模拟 用户登录

手机版页面 [demo_mobile.html](http://gaea.app/static/demo_mobile.html?room_id=101&token=Ah_BRlsZIBbA55axnKWfu0uNwFrtF3ADI8KHM)

PC版页面 [demo.html](http://gaea.app/static/demo.html?room_id=101&token=Ah_BRlsZIBbA55axnKWfu0uNwFrtF3ADI8KHM)

vue手机版页面 [index.html](http://gaea.page/?room_id=101&token=Ah_BRlsZIBbA55axnKWfu0uNwFrtF3ADI8KHM)


# 其他

测试host
```
192.168.1.70       gaea.app
192.168.1.70       gaea.page
```

