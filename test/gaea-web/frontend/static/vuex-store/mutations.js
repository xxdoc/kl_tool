import * as types from "./types.js"

const mutations = {
    [types.RESIZE_VIDEO_BOX](state, payload){
        state.videoBoxSize.width = payload.width
        state.videoBoxSize.height = payload.height
    },
    [types.UPDATE_ROOM_ID](state, payload){
        state.room_id = payload.room_id
    }
}

export default mutations

