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
 * Class ContentTabConfigDao
 * 手机切换菜单配置
 * 数据表 content_tab_config
 * @package tiny_app\Dao
 */
class ContentTabConfigDao
{

    use OrmTrait;

    /**
     * 使用这个特性的子类必须 实现这个方法 返回特定格式的数组 表示数据表的配置
     * @return OrmConfig
     */
    protected static function getOrmConfig()
    {
        if (is_null(static::$_orm_config)) {
            static::$_orm_config = new OrmConfig(Application::getInstance()->getEnv('ENV_MYSQL_DB'), 'content_tab_config', 'room_id', 300, 5000);
        }
        return static::$_orm_config;
    }

    
    /*
     * INTEGER room_id 对应房间 id
     */
    public static function room_id($room_id, $default = null)
    {
        return static::getFiledById('room_id', $room_id, $default);
    }

    
    /*
     * INTEGER content_tab_id 对应 content_tab_id
     */
    public static function content_tab_id($room_id, $default = null)
    {
        return static::getFiledById('content_tab_id', $room_id, $default);
    }

    
    /*
     * VARCHAR(16) active 当前激活的tab栏标题
     */
    public static function active($room_id, $default = null)
    {
        return static::getFiledById('active', $room_id, $default);
    }

    
}