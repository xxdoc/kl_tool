<template>
    <div :style="contentStyle">
        <div class="tab-title">
            <template v-for="tab in tab_list" :active="active"> 
                <span  :class="{ active: tab.title == active }" @click="switch_active(tab)">
                    <img class="new-message" src="./new.png" v-show="tab.new_msg">
                    {{tab.title}}
                </span>
            </template>
        </div>
        <div class="tab-panes" >
            <template v-for="tab in tab_list" :active="active"> 
                <div class="pane" v-show="tab.title == active"> 
                    <keep-alive>
                        <component :is="tab.component" :tab="tab" :active="active"></component>
                    </keep-alive>
                </div>
            </template>
        </div>
    </div>
</template>

<style>
.tab-title {
    width: 100%;
    height: 2.52rem;
    line-height: 2.52rem;
    font-size: 1rem;
    background-color: #E86902;
    z-index: 10;
    position: relative;
    color: #F6C091;
}
.tab-title .active {
    color: #FFFFFF;
    border-bottom: 0.24rem solid #FFFFFF;
}
.tab-title span {
    display: inline-block;
    width: 4.2rem;
    text-align: center;
    height: 2.3rem;
}
.new-message {
    position: absolute;
    width: 0.7rem;
    margin-left: 1.5rem;
    margin-top: 0.5rem;
}
.pane {
    width: 100%;
    position: relative;
    background: #ffffff;
    z-index: 9;
}
</style>

<script>
    import gql from 'graphql-tag'
    import Vuex from "vuex"
    import ChatBox from "../Chat/ChatBox.vue"
    import * as types from "../../vuex-store/types.js"

	export default {
        data(){
            return {
                tab_list: [
                    {title:'聊天', new_msg: false, component: 'chat-box'},
                    {title:'公告', new_msg: true, component: 'notice-box'},
                    {title:'活动', new_msg: true, component: 'plan-box'},
                    {title:'测试', new_msg: true, component: 'test-box'},
                ],
                active: '聊天',
            }
        },
        methods:{
            switch_active:function(tab) {
                this.active = tab.title
                tab.new_msg = false
            }
        },
        computed: {
            contentStyle(){
                return {
                    width: this.contentBoxSize.width + 'px',
                    height: this.contentBoxSize.height + 'px',
                }
            },
            ...Vuex.mapGetters([types.STATE_contentBoxSize]),
        },
        components: {
			ChatBox,
		}
	}
</script>
