<?php
/**
 * Created by table_graphQL.
 * User: Administrator
 * Date: 2017-06
 */
namespace tiny_app\Dao;

use TinyWeb\Application;
use TinyWeb\OrmQuery\OrmConfig;
use TinyWeb\Traits\OrmTrait;


/**
 * Class BasicUserDao
 * 用户信息 不同的用户类型对应不同的权限
 * 数据表 basic_user
 * @package tiny_app\Dao
 */
class BasicUserDao
{

    use OrmTrait;

    /**
     * 使用这个特性的子类必须 实现这个方法 返回特定格式的数组 表示数据表的配置
     * @return OrmConfig
     */
    protected static function getOrmConfig()
    {
        if (is_null(static::$_orm_config)) {
            static::$_orm_config = new OrmConfig(Application::getInstance()->getEnv('ENV_MYSQL_DB'), 'basic_user', 'user_id', 300, 5000);
        }
        return static::$_orm_config;
    }

    
    /*
     * INTEGER user_id 用户 唯一id
     */
    public static function user_id($user_id, $default = null)
    {
        return static::getFiledById('user_id', $user_id, $default);
    }

    
    /*
     * VARCHAR(16) nick 用户昵称
     */
    public static function nick($user_id, $default = null)
    {
        return static::getFiledById('nick', $user_id, $default);
    }

    
    /*
     * VARCHAR(128) avatar 用户头像
     */
    public static function avatar($user_id, $default = null)
    {
        return static::getFiledById('avatar', $user_id, $default);
    }

    
    /*
     * VARCHAR(16) user_type 用户类型 游客 guest, 已认证 authorized, 管理者 manager, 发布者 publisher
     */
    public static function user_type($user_id, $default = null)
    {
        return static::getFiledById('user_type', $user_id, $default);
    }

    
}