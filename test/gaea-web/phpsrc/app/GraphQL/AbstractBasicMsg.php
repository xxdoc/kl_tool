<?php
/**
 * Created by table_graphQL.
 * User: Administrator
 * Date: 2017-06
 */
namespace MyGraphQL;

use MyGraphQL\Type\BasicMsg;

use GraphQL\Type\Definition\ResolveInfo;

/**
 * Class AbstractBasicMsg
 * 互动消息模型 可扩展自定义类型
 * @package MyGraphQL
 */
abstract class AbstractBasicMsg extends BasicMsg
{
    
    /**
     * 互动消息 消息内容
     * ---------------------
     * @param array $rootValue
     * @param array $args
     * @param mixed $context
     * @param ResolveInfo $info
     * @return mixed MsgContentUnion
     */
    abstract public function msgContent($rootValue, $args, $context, ResolveInfo $info);
    
    /**
     * 当前用户信息
     * ---------------------
     * @param array $rootValue
     * @param array $args
     * @param mixed $context
     * @param ResolveInfo $info
     * @return mixed BasicUser
     */
    abstract public function user($rootValue, $args, $context, ResolveInfo $info);
    
}