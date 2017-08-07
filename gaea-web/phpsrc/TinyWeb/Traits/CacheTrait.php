<?php
/**
 * Created by PhpStorm.
 * User: Administrator
 * Date: 2017/3/12 0012
 * Time: 15:26
 */

namespace TinyWeb\Traits;

use TinyWeb\Application;
use phpFastCache\CacheManager;
use TinyWeb\OrmQuery\where;

trait CacheTrait
{
    protected static $_ACTION_DEFAULT = 'load';
    protected static $_ACTION_MAP = [
        'call' => '直接调用，跳过缓存检查，返回结果',
        'clear' => '清除缓存, 无任何返回',
        'load' => '加载数据，优先使用缓存，返回结果',
        'fresh' => '直接调用，强制刷新缓存，返回结果'
    ];
    protected static $_PREFIX_CACHE = 'BMCache';

    private static $_mCacheManager = null;

    protected static function getCacheInstance()
    {
        if (is_null(self::$_mCacheManager)) {
            self::$_mCacheManager = CacheManager::getInstance('files', [
                "path" => Application::getInstance()->getEnv('CACHE_PATH'),
            ]);
        }
        if (empty($mCache)) {
            self::_redisError("CacheManager getInstance error");
        }
        return self::$_mCacheManager;
    }

    /**
     * 使用redis缓存函数调用的结果 优先使用缓存中的数据
     * @param string $method 所在方法 方便检索
     * @param string $key redis 缓存tag 表示分类
     * @param callable $func 获取结果的调用 没有任何参数  需要有返回结果
     * @param callable $filter 判断结果是否可以缓存的调用 参数为 $func 的返回结果 返回值为bool
     * @param string $action 操作类型
     * @param array $tags 标记数组
     * @param string $prefix 缓存键 的 前缀
     * @param bool $is_log 是否显示日志
     * @return array
     * @throws \phpFastCache\Exceptions\phpFastCacheDriverCheckException
     */
    protected static function _cacheDataManager($method, $key, callable $func, callable $filter = null, $action = 'load', array $tags = [], $prefix = null, $is_log = false)
    {
        if (empty($key) || empty($method) || $action == 'call') {
            return $func();
        }
        if (is_null($prefix)) {
            $prefix = static::$_PREFIX_CACHE;
        }
        if (empty(self::$_ACTION_MAP[$action])) {
            $action = static::$_ACTION_DEFAULT;
        }

        $method = str_replace('::', '.', $method);
        $now = time();
        $rKey = !empty($prefix) ? "{$prefix}:{$method}?{$key}" : "{$method}?{$key}";
        $mCache = self::getCacheInstance();

        if ($action == 'clear') {  //需要清除缓存并清除所有相关tags的缓存
            $mCache->deleteItem($rKey);
            !empty($tags) && $mCache->deleteItemsByTags($tags);
            $is_log && self::_redisDebug('delete', $now, $method, $key, 0, $now, $tags);
            return null;
        } else if ($action == 'load') {  //判断缓存有效期是否在要求之内  数据符合要求直接返回  不再执行 func
            $val = $mCache->getItem($rKey)->get() ?: [];
            $data = isset($val['data']) ? $val['data'] : null;
            $update = isset($val['_update_']) ? $val['_update_'] : null;
            $timeCache = $filter($data);
            if (!is_null($data) && !is_null($update) && $now - $update < $timeCache) {
                $is_log && self::_redisDebug('cached', $now, $method, $key, $timeCache, $update, $tags);
                return $data;
            }
        } else if ($action == 'fresh') {  //无任何处理
        }

        $data = $func();
        $timeCache = intval($filter($data));
        if ($timeCache > 0) {   //需要缓存 且缓存世间大于0 保存数据并加上 tags
            $val = ['_update_' => $now, 'data' => $data];
            $itemObj = $mCache->getItem($rKey)->set($val)->expiresAfter($timeCache);
            !empty($tags) && $itemObj->setTags($tags);
            $mCache->save($itemObj);
            $is_log && self::_redisDebug('filter cache', $now, $method, $key, $timeCache, $now, $tags);
        } else {
            $is_log && self::_redisDebug('filter skip', $now, $method, $key, $timeCache, $now, $tags);
        }
        return $data;
    }

    protected static function _redisDebug($action, $now, $method, $key, $timeCache, $update, $tags)
    {
        $log_msg = "{$action} now:{$now}, method:{$method}, key:{$key}, timeCache:{$timeCache}, _update_:{$update}";
        if (!empty($tags)) {
            $log_msg .= ", tags:[" . join(',', $tags) . ']';
        }
        LogTrait::debug($log_msg, __METHOD__, __CLASS__, __LINE__);
    }

    protected static function _redisError($log_msg)
    {
        LogTrait::debug($log_msg, __METHOD__, __CLASS__, __LINE__);
    }
}