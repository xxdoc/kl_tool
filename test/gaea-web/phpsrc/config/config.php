<?php
!defined('ROOT_PATH') && define("ROOT_PATH", dirname(dirname(__FILE__)) . DIRECTORY_SEPARATOR );
require(ROOT_PATH . 'vendor/autoload.php');

if (!defined('SYSTEM_HOST')) {
    ini_set('display_errors', 0);
    ini_set('log_errors', 1);
    date_default_timezone_set('Asia/Shanghai');

    define('SYSTEM_HOST', (isset($_SERVER["HTTPS"]) && $_SERVER["HTTPS"] == "on" ? 'https:' : 'http:') . ( isset($_SERVER['HTTP_HOST']) ? "//{$_SERVER['HTTP_HOST']}/" : '//localhost/') );  //HTTP HOST 常量
}

return [
    'DEV_MODEL' => 'DEBUG',  //开发模式  DEBUG 调试  PRODUCT 产品
    'PLUGIN_PATH' => ROOT_PATH . 'plugin' . DIRECTORY_SEPARATOR,
    'CACHE_PATH' => ROOT_PATH . 'cache' . DIRECTORY_SEPARATOR,  //缓存文件存放地址
    'LOG_PATH' => ROOT_PATH . 'logs' . DIRECTORY_SEPARATOR,  //日志文件存放地址
    'LOG_LEVEL' => 'DEBUG',  //日志记录级别 [ALL, DEBUG, INFO, WARN, ERROR, FATAL, OFF]
];

