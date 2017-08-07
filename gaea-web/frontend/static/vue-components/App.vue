<template>
	<div id="app">
        <template v-if=" room.room_status=='normal' ">
            <player-box player_type="mpsplayer"></player-box>
            <content-box></content-box>
        </template>
        <template v-else-if=" room.room_status=='frozen' ">
            活动已被冻结
        </template>
        <template v-else-if=" room.room_status=='deleted' ">
            活动已被删除
        </template>
        <template v-else-if=" room.room_status=='loading' ">
        </template>
        <template v-else>
            不存在
        </template>
	</div>
</template>

<script>
    import gql from 'graphql-tag'
    import Vuex from "vuex"
    import * as types from "../vuex-store/types.js"

    import PlayerBox from "./Player/PlayerBox.vue"
    import ContentBox from "./Content/ContentBox.vue"

	export default {
        data: function(){
            return {
                room: {
                    room_status: 'loading'
                },
            }
        },
        computed: {
            ...Vuex.mapGetters([types.STATE_room_id]),
        },
        apollo: {
            room: {
                query: gql`query GetRoomStatus($room_id: ID!){
                    room(room_id: $room_id){
                        room_status
                    }
                }`,
                variables(){
                    return {
                        room_id: this.room_id,
                    }
                },
                fetchPolicy: 'network-only',
            }
        },
		components: {
			PlayerBox,
			ContentBox,
		}
	}
</script>
