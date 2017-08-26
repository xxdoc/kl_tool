
import * as types from "./types.js"


const getters = {
	[types.STATE_contentBoxSize](state){
		return {
			width: state.videoBoxSize.width,
			height: document.documentElement.clientHeight - state.videoBoxSize.height
		}
	},
	[types.STATE_contentBoxSizeRem](state){
		return {
			width: state.videoBoxSize.width / state.remSize,
			height: (document.documentElement.clientHeight - state.videoBoxSize.height) / state.remSize
		}
	},
	[types.STATE_videoBoxSize](state){
		return state.videoBoxSize
	},
	[types.STATE_room_id](state){
		return state.room_id
	}
}

export default getters
