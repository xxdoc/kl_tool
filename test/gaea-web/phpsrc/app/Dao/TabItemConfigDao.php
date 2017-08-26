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
 * Class TabItemConfigDao
 * 单个tab选项的配置
 * 数据表 tab_item_config
 * @package tiny_app\Dao
 */
class TabItemConfigDao
{

    use OrmTrait;

    /**
     * 使用这个特性的子类必须 实现这个方法 返回特定格式的数组 表示数据表的配置
     * @return OrmConfig
     */
    protected static function getOrmConfig()
    {
        if (is_null(static::$_orm_config)) {
            static::$_orm_config = new OrmConfig(Application::getInstance()->getEnv('ENV_MYSQL_DB'), 'tab_item_config', 'content_tab_id', 300, 5000);
        }
        return static::$_orm_config;
    }

    
    /*
     * INTEGER content_tab_id 对应 content_tab_id
     */
    public static function content_tab_id($content_tab_id, $default = null)
    {
        return static::getFiledById('content_tab_id', $content_tab_id, $default);
    }

    
    /*
     * VARCHAR(16) title 标题
     */
    public static function title($content_tab_id, $default = null)
    {
        return static::getFiledById('title', $content_tab_id, $default);
    }

    
    /*
     * SMALLINT new_msg 提醒新消息数量
     */
    public static function new_msg($content_tab_id, $default = null)
    {
        return static::getFiledById('new_msg', $content_tab_id, $default);
    }

    
    /*
     * VARCHAR(16) component 对应区域内容类型
     */
    public static function component($content_tab_id, $default = null)
    {
        return static::getFiledById('component', $content_tab_id, $default);
    }

    
}