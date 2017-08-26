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
 * Class PlayerAodianConfigDao
 * 直播活动 奥点播放器
 * 数据表 player_aodian_config
 * @package tiny_app\Dao
 */
class PlayerAodianConfigDao
{

    use OrmTrait;

    /**
     * 使用这个特性的子类必须 实现这个方法 返回特定格式的数组 表示数据表的配置
     * @return OrmConfig
     */
    protected static function getOrmConfig()
    {
        if (is_null(static::$_orm_config)) {
            static::$_orm_config = new OrmConfig(Application::getInstance()->getEnv('ENV_MYSQL_DB'), 'player_aodian_config', 'room_id', 300, 5000);
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
     * VARCHAR(16) player_type 播放器类型 固定为 aodianplayer
     */
    public static function player_type($room_id, $default = null)
    {
        return static::getFiledById('player_type', $room_id, $default);
    }

    
    /*
     * VARCHAR(128) rtmpUrl 控制台开通的APP rtmp地址 必要参数
     */
    public static function rtmpUrl($room_id, $default = null)
    {
        return static::getFiledById('rtmpUrl', $room_id, $default);
    }

    
    /*
     * VARCHAR(128) hlsUrl 控制台开通的APP hls地址 必要参数
     */
    public static function hlsUrl($room_id, $default = null)
    {
        return static::getFiledById('hlsUrl', $room_id, $default);
    }

    
    /*
     * SMALLINT autostart 是否自动播放
     */
    public static function autostart($room_id, $default = null)
    {
        return static::getFiledById('autostart', $room_id, $default);
    }

    
    /*
     * SMALLINT bufferlength 视频缓冲时间 默认为1秒
     */
    public static function bufferlength($room_id, $default = null)
    {
        return static::getFiledById('bufferlength', $room_id, $default);
    }

    
    /*
     * SMALLINT maxbufferlength 最大视频缓冲时间 默认为2秒
     */
    public static function maxbufferlength($room_id, $default = null)
    {
        return static::getFiledById('maxbufferlength', $room_id, $default);
    }

    
    /*
     * SMALLINT stretching 设置全屏模式 1代表按比例撑满至全屏 2代表铺满全屏 3代表视频原始大小
     */
    public static function stretching($room_id, $default = null)
    {
        return static::getFiledById('stretching', $room_id, $default);
    }

    
    /*
     * VARCHAR(16) controlbardisplay 是否显示控制栏 可取值 disable enable 默认为disable
     */
    public static function controlbardisplay($room_id, $default = null)
    {
        return static::getFiledById('controlbardisplay', $room_id, $default);
    }

    
    /*
     * SMALLINT defvolume 默认音量
     */
    public static function defvolume($room_id, $default = null)
    {
        return static::getFiledById('defvolume', $room_id, $default);
    }

    
    /*
     * VARCHAR(128) adveDeAddr 封面图地址
     */
    public static function adveDeAddr($room_id, $default = null)
    {
        return static::getFiledById('adveDeAddr', $room_id, $default);
    }

    
}