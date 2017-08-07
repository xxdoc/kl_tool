<template>
    <div class="dms-container" :style="chatStyle">
        <div class="dms-message-container" id="dms">
            <div class="dmsMessage" :style="chatListStyle">
                <msg-item v-for="(msg, index) in sortMsg(chat_msg_list)" :msg="msg" :key="msg.msg_id"></msg-item>
            </div>
        </div>
        <div class="dms-send-container" >
            <div class="dms-textarea-container">
                <i value="" class="dms-emotion-button" :style="emotionStyle"></i>
                <div class="dms-textarea-box" :style="textareaStyle">
                    <input v-model="message" placeholder="和大家一起聊天吧" type="text"  value="" :style="inputStyle" id="aodianyun-dms-text">
                    <i class="send-btn" :class="{disable: room.chatConfig.review_type=='disable_chat'}" @keyup.enter="sendMsg" @click="sendMsg" :style="sendStyle">发送</i>
                </div>
            </div>
        </div>
    </div>
</template>

<style>
.dms-send-container {
    position: fixed;
    bottom: 0px;
    width: 100%;
    height: 3.6rem;
    color: #000000;
    overflow: hidden;
    background: #D9D9D9;
}
.dms-send-container .dms-textarea-container {
    height: 100%;
    margin-left: 0.44rem;
    padding-top: 0.7rem;
    float: left;
    position: absolute;
}
.dms-textarea-container .dms-textarea-box {
    height: 2.2rem;
    margin-left: .2rem;
    float: left;
}
.dms-textarea-container input[type="text"] {
    float: left;
    margin: 0;
    margin-left: 0.5rem;
    padding: 0;
    resize: none;
    overflow: auto;
    color: #969696;
    font-size: 1rem;
    outline: none;
    padding-left: .2rem;
    height: 2.28rem;
    border: 0.1rem solid rgba(188,188,188,1);
    border-radius: 0.1rem;
    line-height: 2.1rem;
}
.dms-textarea-box .send-btn {
    float: left;
    border: none;
    -webkit-appearance: none;
    outline: none;
    width: 4rem;
    height: 2.2rem;
    background-color: #FF6600;
    text-align: center;
    line-height: 2.2rem;
    color: #FFF;
    margin-left: 0.5rem;
}
.dms-textarea-box .disable{
    background-color: #847D79;
}
.dms-emotion-button {
    float: left;
    margin-top: 0.1rem;
    outline: none;
    background-image: url(./emotion.png);
    display: inline-block;
    background-size: 2rem;
    width: 2rem;
    height: 2rem;
}
.dmsMessage {
    width: 100%;
    padding: 0;
    margin: 0;
    position: relative;
    clear: both;
    overflow: hidden;
    font-size: 1rem;
    color: #676767;
    height: auto;
    overflow-y: scroll;
    /*background: #F1F1F1;*/
}
.swiper-container {
    height: 150px;
    width: 320px;
}
.swiper-container {
    margin: 0 auto;
    position: relative;
    overflow: hidden;
    -webkit-backface-visibility: hidden;
    -moz-backface-visibility: hidden;
    -ms-backface-visibility: hidden;
    -o-backface-visibility: hidden;
    backface-visibility: hidden;
    z-index: 1;
}
.swiper-wrapper {
    position: relative;
    width: 100%;
    -webkit-transition-property: -webkit-transform, left, top;
    -webkit-transition-duration: 0s;
    -webkit-transform: translate3d(0px,0,0);
    -webkit-transition-timing-function: ease;
    -moz-transition-property: -moz-transform, left, top;
    -moz-transition-duration: 0s;
    -moz-transform: translate3d(0px,0,0);
    -moz-transition-timing-function: ease;
    -o-transition-property: -o-transform, left, top;
    -o-transition-duration: 0s;
    -o-transform: translate3d(0px,0,0);
    -o-transition-timing-function: ease;
    -o-transform: translate(0px,0px);
    -ms-transition-property: -ms-transform, left, top;
    -ms-transition-duration: 0s;
    -ms-transform: translate3d(0px,0,0);
    -ms-transition-timing-function: ease;
    transition-property: transform, left, top;
    transition-duration: 0s;
    transform: translate3d(0px,0,0);
    transition-timing-function: ease;
}
/*手机表情滑动*/
.swiper-active-switch {
    background: #fff !important;
}
.swiper-pagination-switch {
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 10px;
    background: #999;
    box-shadow: 0px 1px 2px #555 inset;
    margin: 0 3px;
    cursor: pointer;
}
</style>

<script>
    import gql from 'graphql-tag'
    import Vuex from "vuex"
    import * as types from "../../vuex-store/types.js"
    import MsgItem from "./MsgItem.vue"

	export default {
        data(){
            return {
                message: '',
                chat_msg_list: [],
                room: {
                    chatConfig: {
                        review_type: 'loading'
                    }
                },
                em_path: '/static/images/arclist/' //表情存放的路径
            }
        },
        props: ['tab', 'active'],
        created(){
            //表情
            $('#aodianyun-dms-text').wait(()=> {
                $('.dms-emotion-button').qqFace({
                    id:'facebox',
                    assign:'aodianyun-dms-text',
                    path: this.em_path
                })
            })

            this.$store.dms.onMsg('chat_and_review', (topic, dms_data) => {
                this.appentMsgList(dms_data);
            }, (topic, dms_data) => {
                return dms_data.msgContent.msg_status =='publish_chat';
            });
        },
        apollo: {
            room: {
                query: gql`query GetChatConfig($room_id: ID!){
                    room(room_id: $room_id){
                        chatConfig{
                            review_type
                        },
                    }
                }`,
                variables(){
                    return {
                        room_id: this.room_id,
                    }
                },
                fetchPolicy: 'network-only'
            }
        },
        methods:{
            sortMsg(list){
                var tmp = [
                    ... list
                ]
                return tmp.sort((a, b) => a.msg_id > b.msg_id)
            },
            replaceEm(str){
                str = str.replace(/\</g, '&lt;')
                str = str.replace(/\>/g, '&gt;')
                str = str.replace(/\n/g, '<br/>')
                str = str.replace(/\[em_([0-9]*)\]/g, '<img src="' + this.em_path + '$1.gif" border="0" style="vertical-align: middle;width: 24px;"/>')
                return str
            },
            appentMsgList(dmsMsg){
                if(dmsMsg.msgContent.msg_status =='publish_chat' && this.chat_msg_list.filter((msg)=> msg.msg_id==dmsMsg.msg_id).length==0){
                    if( dmsMsg.msgContent.content_text ){
                        dmsMsg.msgContent.content_html = this.replaceEm(dmsMsg.msgContent.content_text)
                    }
                    this.chat_msg_list.push(dmsMsg)
                    if( this.tab.title != this.active ){
                        this.tab.new_msg = true
                    }
                }
            },
            sendMsg(){
                if( this.room.chatConfig.review_type=='disable_chat' ){
                    return
                }
                var message = $('#aodianyun-dms-text').val()
                if( message=='' ){
                    alert('消息不可为空')
                    return
                }
                message = message.replace(/\[([\u4e00-\u9fa5]{1,})\]/g, function(){
                    if (typeof(dmsFaceArr2[arguments[1]]) == 'undefined') {
                        return arguments[0];
                    } else {
                        return '[' + dmsFaceArr2[arguments[1]] + ']';
                    }
                })

                var dmsMsg = {
                    room_id: this.room_id,
                    msg_type: 'chat_and_review',
                    msgContent: {
                        msg_status: 'publish_chat',
                        target_user_id: null,
                        content_text: message
                    }
                }
                this.$store.dms.dmsMsgPublish(dmsMsg, (data) => {
                    this.appentMsgList(data.dmsMsg)
                    this.message = ''
                },(data) => {
                    alert(data.FlagString)
                })
            }
        },
        computed: {
            chatStyle(){
                return {
                    height: this.contentBoxSizeRem.height - 2.52 + 'rem',
                    width: this.contentBoxSizeRem.width + 'rem'
                }
            },
            emotionStyle(){
                return {
                }
            },
            textareaStyle(){
                return {
                    width: this.contentBoxSizeRem.width - 3 + 'rem'
                }
            },
            inputStyle(){
                return {
                    width: this.contentBoxSizeRem.width - 8.5 + 'rem'
                }
            },
            chatListStyle(){
                return {
                    height: this.contentBoxSizeRem.height - 2.52 - 3.6 + 'rem',
                }
            },
            sendStyle(){
                return {

                }
            },
            ...Vuex.mapGetters([types.STATE_room_id, types.STATE_contentBoxSizeRem]),
        },
		components: {
			MsgItem,
		}
	}
</script>
