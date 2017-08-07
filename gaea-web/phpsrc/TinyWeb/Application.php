<?php
/**
 * Created by PhpStorm.
 * User: Administrator
 * Date: 2017/6/13 0013
 * Time: 22:13
 */

namespace TinyWeb;


use PhpConsole\Connector;

final class Application
{
    private static $_instance = null;  // Application实现单利模式, 此属性保存当前实例
    private static $_request_microtime = null;
    private static $_dev_model = 'PRODUCT';

    /**
     * Application constructor.
     * @param array $config 关联数组的配置
     */
    public function __construct(array $config = [])
    {
        $this->_config = $config;
        self::$_instance = $this;
    }

    public static function enableDebugModel()
    {
        self::$_dev_model = 'DEBUG';
    }

    public static function isDebugModel()
    {
        return self::$_dev_model == 'DEBUG';
    }

    public static function usedMilliSecond()
    {
        if (is_null(self::$_request_microtime)) {
            self::$_request_microtime = microtime(true);
            return 0;
        }
        return round(microtime(true) - self::$_request_microtime, 3) * 1000;
    }

    /**
     * 获取当前的Application实例
     * @return Application
     */
    public static function getInstance()
    {
        if (is_null(self::$_instance)) {
            self::$_instance = new self();
        }
        return self::$_instance;
    }

    /**
     * 获取 全局配置 指定key的值 不存在则返回 default
     * @param string $key
     * @param mixed $default
     * @return mixed
     */
    public function getEnv($key, $default = '')
    {
        return isset($this->_config[$key]) ? $this->_config[$key] : $default;
    }

    /**
     * 调试使用 开发模式下有效
     * @param array $data
     * @param string|null $tags
     * @param int $ignoreTraceCalls
     */
    public static function _D($data, $tags = null, $ignoreTraceCalls = 0)
    {
        if (self::isDebugModel()) {
            if (!empty($tags)) {
                $tags = strval($tags) . ':' . self::usedMilliSecond() . 'ms';
            }
            Connector::getInstance()->getDebugDispatcher()->dispatchDebug($data, $tags, $ignoreTraceCalls);
        }
    }
}