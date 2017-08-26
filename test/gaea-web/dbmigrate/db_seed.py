# coding: utf-8
import random, time, datetime, json

from app import db, models, md5key

def _save(tbl, items, filter_by=None, primary_key=''):
    all_num, save_num = len(items), 0
    print "\n", 'SAVE %r, len:%d, filter_by:%r, primary_key:%s' % (tbl, all_num, filter_by, primary_key)
    if filter_by is None and primary_key:
        def filter_by(item):
            return tbl.query.filter_by(**{primary_key: item[primary_key]}).first()

    for item in items:
        if filter_by and not filter_by(item):
            print '.',
            save_num += 1
            db.session.add( tbl(**item) )
        else:
            print 'x',
    db.session.commit()
    print "\n", 'COMMIT all:%d, save:%d' % (all_num, save_num)

def _BasicRoom(idx):
    return {
        'room_id': idx,
        'room_title': 'live test %s' % (idx, ),
        'chat_topic': 'room_%s' % (idx, ),
        'dms_sub_key': 'sub_eae37e48dab5f305516d07788eaaea60',
        'dms_pub_key': 'pub_5bfb7a0ced7adb2ce454575747762679',
        'dms_s_key': 's_ceb80d29276f78653df081e5a9f0ac76',
        'aodian_uin': '13830',
        'lss_app': 'dyy_1736_133',
        'stream': 'a0c3d2dd3b4688f31da13991477980d9',
        'room_status': 1,
    }

BasicRoom_list = [_BasicRoom(idx) for idx in range(101, 106)]
_save(models.BasicRoom, BasicRoom_list, primary_key='room_id')

def _ChatConfig(idx):
    return {
        'room_id': idx,
        'review_type': 'direct_pub',
        'sysmsg_type': 'show_all',
    }

ChatConfig_list = [_ChatConfig(BasicRoom_tmp['room_id']) for BasicRoom_tmp in BasicRoom_list]
_save(models.ChatConfig, ChatConfig_list, primary_key='room_id')

def _PlayerAodianConfig(idx):
    return {
        'room_id': idx,
        'player_type': 'aodianplayer',
        'rtmpUrl': 'rtmp://13830.lssplay.aodianyun.com/dyy_1736_133/a0c3d2dd3b4688f31da13991477980d9',
        'hlsUrl': 'http://13830.hlsplay.aodianyun.com/dyy_1736_133/a0c3d2dd3b4688f31da13991477980d9.m3u8',
        'autostart': 1,
        'bufferlength': 1,
        'maxbufferlength': 1,
        'stretching': 1,
        'controlbardisplay': 'enable',
        'defvolume': 80,
        'adveDeAddr': 'http://static.douyalive.com/aae/dyy/assets/img/play_bj.png',
    }

PlayerAodianConfig_list = [_PlayerAodianConfig(BasicRoom_tmp['room_id']) for BasicRoom_tmp in BasicRoom_list]
_save(models.PlayerAodianConfig, PlayerAodianConfig_list, primary_key='room_id')

def _PlayerMpsConfig(idx):
    return {
        'room_id': idx,
        'player_type': 'mpsplayer',
        'uin': 13830,
        'appId': 'fHNNBuuB3BbUWJiP',
        'autostart': 1,
        'stretching': 1,
        'mobilefullscreen': 0,
        'controlbardisplay': 'enable',
        'isclickplay': 1,
        'isfullscreen': 1,
    }

PlayerMpsConfig_list = [_PlayerMpsConfig(BasicRoom_tmp['room_id']) for BasicRoom_tmp in BasicRoom_list]
_save(models.PlayerMpsConfig, PlayerMpsConfig_list, primary_key='room_id')

def _BasicUser(idx):
    return {
        'user_id': idx,
        'nick': 'Nick%s' % (idx, ),
        'avatar': 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png',
        'user_type': 'authorized',
    }

BasicUser_list = [_BasicUser(idx) for idx in range(10000, 10100)] + [
{
    'user_id': 1000,
    'nick': 'Mgr%s' % (1000, ),
    'avatar': 'http://58jinrongyun.com/dist/dyy/view/jiaoyu/mobile/images/male.png',
    'user_type': 'manager',
}
]

_save(models.BasicUser, BasicUser_list, primary_key='user_id')


random_msg_str = lambda str_list= ['AAA', 'BBB', 'CCC', 'ABC', 'DEF', 'QWE', 'ASD', 'DEF'] : random.choice(str_list)
random_msg_status = lambda status_list= ['publish_chat', 'review_pub', 'review_del', 'review_add'] : random.choice(status_list)
random_trade_type = lambda type_list = ['RMB', 'USD', 'gift_car', 'gift_666', 'gift_plane']: random.choice(type_list)


def _BasicMsg(idx):
    return {
        'msg_id': idx,
        'room_id': random.choice(BasicRoom_list)['room_id'],
        'user_id': random.choice(BasicUser_list)['user_id'],
        'msg_type': 'chat_and_review',
        'timestamp': int(time.time()) + random.randint(-1000, 1000),
    }

BasicMsg_list = [_BasicMsg(idx) for idx in range(20000, 20200)]
_save(models.BasicMsg, BasicMsg_list, primary_key='msg_id')

def _MsgChatAndReView(idx):
    msg_status = 'review_add' if idx % 100 == 0 else \
                    'review_del' if idx % 100 == 1 else random_msg_status()
    target_user_id = random.choice(BasicUser_list)['user_id'] if idx % 100 == 2 else ''
    target_msg_id = idx - 1 if idx % 100 == 1 else 0
    operator_id = 1000 if idx % 100 == 1 else ''
    return {
        'msg_id': idx,
        'msg_type': 'chat_and_review',
        'target_user_id': target_user_id,
        'target_msg_id': target_msg_id,
        'content_text': random_msg_str(),
        'msg_status': msg_status,
        'operator_id': operator_id,
    }

MsgChatAndReView_list = [_MsgChatAndReView(BasicMsg_tmp['msg_id']) for BasicMsg_tmp in BasicMsg_list]
_save(models.MsgChatAndReView, MsgChatAndReView_list, primary_key='msg_id')


def _BasicMsg(idx):
    return {
        'msg_id': idx,
        'room_id': random.choice(BasicRoom_list)['room_id'],
        'user_id': random.choice(BasicUser_list)['user_id'],
        'msg_type': 'donate_and_gift',
        'timestamp': int(time.time()) + random.randint(-1000, 1000),
    }

BasicMsg_list = [_BasicMsg(idx) for idx in range(30000, 30200)]
_save(models.BasicMsg, BasicMsg_list, primary_key='msg_id')

def _MsgDonateAndGift(idx):
    trade_type = random_trade_type()
    trade_num = round(random.random() * 1000, 2) if trade_type=='RMB' or trade_type=='USD' else random.randint(1, 1000)
    return {
        'msg_id': idx,
        'msg_type': 'donate_and_gift',
        'target_user_id': random.choice(BasicUser_list)['user_id'],
        'content_text': '%s (x %s) ps:%s' % (trade_type, trade_num, random_msg_str()),
        'trade_type': trade_type,
        'trade_num': trade_num,
    }

MsgDonateAndGift_list = [_MsgDonateAndGift(BasicMsg_tmp['msg_id']) for BasicMsg_tmp in BasicMsg_list]
_save(models.MsgDonateAndGift, MsgDonateAndGift_list, primary_key='msg_id')
