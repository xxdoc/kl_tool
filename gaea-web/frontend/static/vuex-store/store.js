import Vue from "vue"
import Vuex from "vuex"
import mutations from "./mutations.js"
import actions from "./actions.js"
import getters from "./getters.js"

Vue.use(Vuex)

const state = {
    room_id: 0,
    remSize: parseFloat($('html').css('font-size')),
    videoBoxSize: {
        width: document.documentElement.clientWidth,
        height: document.documentElement.clientWidth / 852 * 480
    }
}

export default new Vuex.Store({
    dms: null,
	state,
	mutations,
	actions,
	getters,
})