import 'babel-polyfill'
import Vue from "vue"
import Vuex from "vuex"
import gql from 'graphql-tag'

import * as types from "./vuex-store/types.js"
import store from "./vuex-store/store.js"
import App from "./vue-components/App.vue"

import { ApolloClient, createNetworkInterface } from 'apollo-client'
import VueApollo from 'vue-apollo'

Vue.use(VueApollo)

// Create the apollo client
const apolloClient = new ApolloClient({
  networkInterface: createNetworkInterface({
    uri: 'http://gaea.app/api/GraphQLApi/exec?token=' + ($_GET['token'] ? $_GET['token'] : ''),
  }),
  connectToDevTools: true,
})

store.dms = new DmsHub({
    debug: true,
    token: $_GET['token'] ? $_GET['token'] : ''
})
store.dms.setDmsMsgPublish(function(dmsMsg, success, failure, logHandler, logLevelHandler) {
    store.dms.api_ajax(
        'gaea.app',
        '/api/MsgProxy/publish',
        {
            dmsMsg: dmsMsg,
            token: $_GET['token'] ? $_GET['token'] : ''
        },
        function(res) {
            success(res);
        },
        failure, logHandler, logLevelHandler
    );
})
store.dms.setResolveUser((uid, callback) => {
    apolloClient.query({
        query: gql`query GetUserInfo($user_id: ID!){
            user($room_id: ID!, user_id: $user_id){
                user_id,
                nick,
                avatar,
                user_type,
            }
        }`,
        variables:{
            room_id: $_GET['room_id'] ? parseInt($_GET['room_id']) : 0,
            user_id: uid
        },
        fetchPolicy: 'network-only',
    })
    .then(({ data, loader, networkStatus }) => {
        if(data && data.user){
            typeof callback == 'function' && callback(data.user)
        }
    })
    .catch((error) => {
        console.error(error)
    })
})

apolloClient.query({
    query: gql`query GetDmsConfig($room_id: ID!){
        room(room_id: $room_id){
            room_id,
            room_status,
            room_title,
            chatConfig{
                review_type
            },
            dms_sub_key,
            lss_app,
            stream,
            chat_topic,
            present_topic,
            sync_room_topic,
            sync_user_topic,
            sys_notify_lss_topic,
            currentUser{
                user{
                    user_id,
                    nick,
                    avatar,
                    user_type,
                }
                user_agent,
                client_id
            }
        }
    }`,
    variables:{
        room_id: $_GET['room_id'] ? parseInt($_GET['room_id']) : 0
    },
    fetchPolicy: 'network-only',
})
.then(({ data, loader, networkStatus }) => {
    store.dms.setDmsConfig(data.room)
})
.catch((error) => {
    console.error(error)
})

store.dms.onEnter( data => console.log(data) )
store.dms.onLeave( data => console.log(data) )

const apolloProvider = new VueApollo({
  defaultClient: apolloClient,
})

let app = new Vue({
    el: '#app',
    created: function() {
        var room_id = $_GET['room_id'] ? parseInt($_GET['room_id']) : 0
        this.$store.commit(types.UPDATE_ROOM_ID, {room_id: room_id})
    },
    computed: {
        ...Vuex.mapGetters([types.STATE_room_id]),
    },
    methods: {
        ...Vuex.mapMutations([types.UPDATE_ROOM_ID])
    },
    apolloProvider,
    store,
    render: h => h(App),
})
