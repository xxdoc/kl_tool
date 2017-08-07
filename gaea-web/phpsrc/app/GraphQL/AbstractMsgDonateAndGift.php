<?php
/**
 * Created by table_graphQL.
 * User: Administrator
 * Date: 2017-06
 */
namespace MyGraphQL;

use MyGraphQL\Type\MsgDonateAndGift;

use GraphQL\Type\Definition\ResolveInfo;

/**
 * Class AbstractMsgDonateAndGift
 * 打赏及赠送礼物消息
 * @package MyGraphQL
 */
abstract class AbstractMsgDonateAndGift extends MsgDonateAndGift
{
    
    /**
     * 目标用户 信息
     * ---------------------
     * @param array $rootValue
     * @param array $args
     * @param mixed $context
     * @param ResolveInfo $info
     * @return mixed BasicUser
     */
    abstract public function target_user($rootValue, $args, $context, ResolveInfo $info);
    
}