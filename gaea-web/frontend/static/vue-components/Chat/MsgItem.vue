<template>
    <div class="dms-message-info" :data-msg_id="msg.msg_id">
        <p class="u-dms-message">            
            <img class="dms-head" :src="msg.user.avatar">            
            <span class="dms-date">{{time_str}}</span>            
            <span class="dms-nick" title="YK-48935">{{msg.user.nick}}({{msg.user.user_id}})</span>            
            <span class="dms-content" v-html="content_html"></span>            
        </p>        
    </div>
</template>

<style>

.dms-message-info{
    width: 100%;
    height: auto;
    margin-top: 0.5rem;
    margin-bottom: 0.5rem;
    font-size: 14px;
    float: left;
}
.dms-message-info .u-dms-message{
    margin: 0 5px;
    padding: 0 auto;
    word-break: break-all;
    word-wrap: break-word;
}
.dms-message-info .dms-time{
    margin-right: 5px;
    color: #020203; 
}
.dms-message-info .dms-head{
    width: 1.9rem;
    height: 1.9rem;
    border-radius: 50%;
    float: left;
    margin-left: 0.5rem;
    margin-right: 0.5rem;
}
.dms-message-info .dms-date{
    color: #929292;
    float: left;
    font-size: 0.8rem;
    line-height: 1rem;
    margin-right: 0.3rem;
}
.dms-message-info .dms-nick{
    color: #929292;
    float: left;
    font-size: 0.8rem;
    line-height: 1rem;
}

.dms-message-info .dms-content{
    width: 80%;
    width: calc(100% - 3.2rem);
    width: -webkit-calc(100% - 3.2rem);
    float: left;
    font-size: 1.1rem;
    line-height: 1.4rem;
}
.dms-message-info .dms-content .dms-content-img{
    width: 1.4rem;
}
.dms-message-info .f-dms-content{
    color: #2c2b2b;
    padding-left:0;
}
.dms-message-info .dms-content img{ 
    vertical-align: bottom;
}
.dms-message-info .dms-giftshow{
    width: 1.5rem;
    margin-left: 0.4rem;
}
</style>

<script>

	export default {
        props: ['msg'],
        methods:{
        },
        computed: {
            time_str(){
                return this.$store.dms.date('H:i', this.msg.timestamp)
            },
            content_html(){
                return this.msg.msgContent.content_html
            }
        }
	}
</script>
