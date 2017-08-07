# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Index, Integer, SmallInteger, String, Text


from app import db, app
Base = db.Model


class BasicMsg(Base):
    __tablename__ = 'basic_msg'

    msg_id = Column(Integer, primary_key=True, doc=u"""自增主键""")
    room_id = Column(Integer, nullable=False)
    user_id = Column(String(16), nullable=False)
    msg_type = Column(String(16), nullable=False)
    timestamp = Column(Integer)


class BasicRoom(Base):
    __tablename__ = 'basic_room'

    room_id = Column(Integer, primary_key=True, doc=u"""自增主键""")
    room_title = Column(String(32), nullable=False)
    chat_topic = Column(String(32), nullable=False)
    dms_sub_key = Column(String(64), nullable=False)
    dms_pub_key = Column(String(64), nullable=False)
    dms_s_key = Column(String(64), nullable=False)
    aodian_uin = Column(Integer, nullable=False)
    lss_app = Column(String(32), nullable=False)
    stream = Column(String(32), nullable=False)
    room_status = Column(SmallInteger, nullable=False)


class BasicUser(Base):
    __tablename__ = 'basic_user'

    user_id = Column(Integer, primary_key=True, doc=u"""自增主键""")
    nick = Column(String(16), nullable=False)
    avatar = Column(String(128), nullable=False)
    user_type = Column(String(16), nullable=False)


class ChatConfig(Base):
    __tablename__ = 'chat_config'

    room_id = Column(Integer, primary_key=True, doc=u"""自增主键""")
    review_type = Column(String(16), nullable=False)
    sysmsg_type = Column(String(16), nullable=False)


class ContentTabConfig(Base):
    __tablename__ = 'content_tab_config'

    room_id = Column(Integer, primary_key=True, doc=u"""自增主键""")
    content_tab_id = Column(Integer, nullable=False)
    active = Column(String(16), nullable=False)


class MsgChatAndReview(Base):
    __tablename__ = 'msg_chat_and_review'

    msg_id = Column(Integer, primary_key=True, doc=u"""自增主键""")
    msg_type = Column(String(16), nullable=False)
    target_user_id = Column(String(16), nullable=False)
    target_msg_id = Column(String(16), nullable=False)
    content_text = Column(String(512), nullable=False)
    msg_status = Column(String(16), nullable=False)
    operator_id = Column(String(16))


class MsgDonateAndGift(Base):
    __tablename__ = 'msg_donate_and_gift'

    msg_id = Column(Integer, primary_key=True, doc=u"""自增主键""")
    msg_type = Column(String(16), nullable=False)
    target_user_id = Column(String(16), nullable=False)
    trade_type = Column(String(16), nullable=False)
    trade_num = Column(Float, nullable=False)
    content_text = Column(String(512), nullable=False)


class PlayerAodianConfig(Base):
    __tablename__ = 'player_aodian_config'

    room_id = Column(Integer, primary_key=True, doc=u"""自增主键""")
    player_type = Column(String(16), nullable=False)
    rtmpUrl = Column(String(128), nullable=False)
    hlsUrl = Column(String(128), nullable=False)
    autostart = Column(SmallInteger, nullable=False)
    bufferlength = Column(SmallInteger, nullable=False)
    maxbufferlength = Column(SmallInteger, nullable=False)
    stretching = Column(SmallInteger, nullable=False)
    controlbardisplay = Column(String(16), nullable=False)
    defvolume = Column(SmallInteger, nullable=False)
    adveDeAddr = Column(String(128), nullable=False)


class PlayerMpsConfig(Base):
    __tablename__ = 'player_mps_config'

    room_id = Column(Integer, primary_key=True, doc=u"""自增主键""")
    player_type = Column(String(16), nullable=False)
    uin = Column(Integer, nullable=False)
    appId = Column(String(32), nullable=False)
    autostart = Column(SmallInteger, nullable=False)
    stretching = Column(SmallInteger, nullable=False)
    mobilefullscreen = Column(SmallInteger, nullable=False)
    controlbardisplay = Column(String(16), nullable=False)
    isclickplay = Column(SmallInteger, nullable=False)
    isfullscreen = Column(SmallInteger, nullable=False)


class TabItemConfig(Base):
    __tablename__ = 'tab_item_config'

    content_tab_id = Column(Integer, primary_key=True, doc=u"""自增主键""")
    title = Column(String(16), nullable=False)
    new_msg = Column(SmallInteger, nullable=False)
    component = Column(String(16), nullable=False)
