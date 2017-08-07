<?php
{%- set namespace = options.namespace(options.path) %}
{%- set classname = options.classname(table) %}
/**
 * Created by table_graphQL.
 * User: Administrator
 * Date: {{ time.strftime('%Y-%m') }}
 */
namespace {{ namespace }};

use TinyWeb\Application;
use TinyWeb\OrmQuery\OrmConfig;
use TinyWeb\Traits\OrmTrait;


/**
 * Class {{ classname }}
 * {{ table.class_.__doc__ }}
 * 数据表 {{ table.class_.__tablename__ }}
 * @package {{ namespace }}
 */
class {{ classname }}
{

    use OrmTrait;

    /**
     * 使用这个特性的子类必须 实现这个方法 返回特定格式的数组 表示数据表的配置
     * @return OrmConfig
     */
    protected static function getOrmConfig()
    {
        if (is_null(static::$_orm_config)) {
            static::$_orm_config = new OrmConfig(Application::getInstance()->getEnv('ENV_MYSQL_DB'), '{{ table.class_.__tablename__ }}', '{{ table.primary_key[0].name }}', 300, 5000);
        }
        return static::$_orm_config;
    }

    {% for name, column in table.columns.items() %}
    /*
     * {{ column.type }} {{  name }} {{ column.doc }}
     */
    public static function {{ name }}(${{ table.primary_key[0].name }}, $default = null)
    {
        return static::getFiledById('{{ name }}', ${{ table.primary_key[0].name }}, $default);
    }

    {% endfor %}
}