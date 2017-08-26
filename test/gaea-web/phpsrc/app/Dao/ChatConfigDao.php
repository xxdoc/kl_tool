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
 * Class ChatConfigDao
 * 直播活动 聊天配置信息
 * 数据表 chat_config
 * @package tiny_app\Dao
 */
class ChatConfigDao
{

    use OrmTrait;

    /**
     * 使用这个特性的子类必须 实现这个方法 返回特定格式的数组 表示数据表的配置
     * @return OrmConfig
     */
    protected static function getOrmConfig()
    {
        if (is_null(static::$_orm_config)) {
            static::$_orm_config = new OrmConfig(Application::getInstance()->getEnv('ENV_MYSQL_DB'), 'chat_config', 'room_id', 300, 5000);
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
     * VARCHAR(16) review_type 房间聊天审核类型 禁止聊天 disable_chat, 关闭聊天审核，聊天直接发布 direct_pub, 开启聊天审核 review_chat
     */
    public static function review_type($room_id, $default = null)
    {
        return static::getFiledById('review_type', $room_id, $default);
    }

    
    /*
     * VARCHAR(16) sysmsg_type 房间系统消息显示类型 全部显示 show_all, 全部隐藏 hide_all
     */
    public static function sysmsg_type($room_id, $default = null)
    {
        return static::getFiledById('sysmsg_type', $room_id, $default);
    }

    
}