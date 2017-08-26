<?php
/**
 * Created by table_graphQL.
 * User: Administrator
 * Date: 2017-06
 */
namespace MyGraphQL\Type;

use MyGraphQL\Types;
use GraphQL\Type\Definition\ObjectType;
use GraphQL\Type\Definition\ResolveInfo;

/**
 * Class ContentTabConfig
 * 手机切换菜单配置
 * @package MyGraphQL\Type
 */
class ContentTabConfig extends ObjectType
{

    public function __construct(array $_config = [], $type = null)
    {
        if (is_null($type)) {
            /** @var Types $type */
            $type = new Types();
        }
        $config = [
            'description' => "手机切换菜单配置",
            'fields' => []
        ];
        $config['fields']['active'] = [
            'type' => $type::nonNull($type::String()),
            'description' => "当前激活的tab栏标题",
        ];
        $config['fields']['tabList'] = [
            'type' => $type::listOf($type::TabItemConfig([], $type)),
            'description' => "tab栏列表",
        ];
        
        $config['resolveField'] = function($value, $args, $context, ResolveInfo $info) {
            if (method_exists($this, $info->fieldName)) {
                return $this->{$info->fieldName}($value, $args, $context, $info);
            } else {
                return is_array($value) ? $value[$info->fieldName] : $value->{$info->fieldName};
            }
        };
        if (!empty($_config['fields'])) {
            $config['fields'] = array_merge($_config['fields'], $config['fields']);
        }
        parent::__construct($config);
    }

}