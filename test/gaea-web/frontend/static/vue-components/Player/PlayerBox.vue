<template>
    <div :data-player-type="room.playerConfig.player_type" :style="playerStyle" >
	    <div id="gaea-player-box"></div>
        <div v-show=" room.playerConfig.player_type=='loading' " :style="loadingStyle" >{{loadingText}}</div>
    </div>
</template>



<script>
    import gql from 'graphql-tag'
    import Vuex from "vuex"
    import * as types from "../../vuex-store/types.js"


    function load_player(vm, playerConfig){
            var conf = {
                container: vm.container,
                playCallback: () => {
                    setTimeout(
                        () => {
                            console.log && console.log("playCallback size:", $('#' + vm.container).width(), $('#' + vm.container).height());
                            vm.$store.commit(types.RESIZE_VIDEO_BOX, {
                                width: $('#' + vm.container).width(), 
                                height: $('#' + vm.container).height()
                            })
                        }
                        ,1000);
                },
                pauseCallback: () => {
                    setTimeout(
                        () => {
                            console.log && console.log("pauseCallback size:", $('#' + vm.container).width(), $('#' + vm.container).height());
                            vm.$store.commit(types.RESIZE_VIDEO_BOX, {
                                width: $('#' + vm.container).width(), 
                                height: $('#' + vm.container).height()
                            })
                        }
                        ,1000);
                },
                onload: () => {
                    //可以在这里增加 播放器事件的 回调函数  不同浏览器支持的事件不同
                    console.log && console.log("PlayerReady size:", $('#' + vm.container).width(), $('#' + vm.container).height());
                    vm.$store.commit(types.RESIZE_VIDEO_BOX, {
                        width: $('#' + vm.container).width(), 
                        height: $('#' + vm.container).height()
                    })
                    if(!vm.player.addPlayerCallback){
                        return;
                    }
                    vm.player.addPlayerCallback('start', function(){  // lssplayer 支持 hlsplayer 支持
                        console.log && console.log("PlayerCallback start");
                    });
                    vm.player.addPlayerCallback('full', function(){  // lssplayer 支持 hlsplayer 支持
                        console.log && console.log("PlayerCallback full");
                    });
                    vm.player.addPlayerCallback('empty', function(){  // lssplayer 支持 hlsplayer 支持
                        console.log && console.log("PlayerCallback empty");
                    });
                    vm.player.addPlayerCallback('pause', function(){  // lssplayer 支持 hlsplayer 支持
                        console.log && console.log("PlayerCallback pause");
                    });
                    vm.player.addPlayerCallback('resume', function(){  // lssplayer 支持 hlsplayer 支持
                        console.log && console.log("PlayerCallback resume");
                    });
                    vm.player.addPlayerCallback('stop', function(){  // lssplayer 支持 hlsplayer 支持
                        console.log && console.log("PlayerCallback stop");
                    });

                    vm.player.addPlayerCallback('ready', function(){   //  hlsplayer 支持
                        console.log && console.log("PlayerCallback ready");
                    });
                    vm.player.addPlayerCallback('slider.start', function(){  //hlsplayer 支持
                        console.log && console.log("PlayerCallback slider.start");
                    });
                    thvmis.player.addPlayerCallback('slider.end', function(){   //hlsplayer 支持
                        console.log && console.log("PlayerCallback slider.end");
                    });
                    vm.player.addPlayerCallback('play.stop', function(){   //hlsplayer 支持
                        console.log && console.log("PlayerCallback play.stop");
                    });
                },
                onReady: () => {
                    var tmp = vm.onloaded;
                    vm.onloaded = true;
                    !tmp && typeof(conf.onload) == 'function' && conf.onload.call(vm.player);
                },
                ... playerConfig
            }
            $('#' + vm.container).wait(() => {
                var _map = {
                    'aodianplayer': {
                        playerFunName: 'aodianPlayer',
                        playerFunUrl: 'http://cdn.aodianyun.com/lss/aodianplay/player.js',
                    },
                    'mpsplayer': {
                        playerFunName: 'mpsPlayer',
                        playerFunUrl: 'http://cdn.aodianyun.com/mps/v1/lssplayer.js',
                    }
                }
                var playerFunName = _map[vm.player_type].playerFunName
                var playerFunUrl = _map[vm.player_type].playerFunUrl

                var initPlayer = () => {
                    vm.player = new window[playerFunName](conf)
                    var onReadyTryCount = 0
                    var onReadyInterval = setInterval(() => {
                        onReadyTryCount += 1
                        if ( vm.player.handle || onReadyTryCount >= 500 ) {  //最多等待50s 强制尝试调用onloaded
                            clearInterval(onReadyInterval)
                            conf.onReady()
                        }
                    }, 100)
                }

                if (playerFunName in window && typeof window[playerFunName] == "function") {
                    initPlayer()
                } else {
                    var layoutScript = document.createElement('script')
                    layoutScript.type = 'text/javascript'
                    layoutScript.charset = 'UTF-8'
                    layoutScript.src = playerFunUrl
                    document.getElementsByTagName("body")[0].appendChild(layoutScript)
                    var playerLoadInterval = setInterval(() => {
                        if (playerFunName in window && typeof window[playerFunName] == "function") {
                            clearInterval(playerLoadInterval)
                            initPlayer()
                        }
                    }, 100)
                }
            })
    }

	export default {
        player: null,
        data: function(){
            return {
                container: 'gaea-player-box',
                onloaded: false,
                room: {
                    playerConfig: {
                        player_type: 'loading'
                    }
                },
                loadingText: '加载中。。。',
            }
        },
        props: ['player_type'],
        created() {
        },
        computed: {
            playerStyle(){
                return {
                    width: this.videoBoxSize.width + 'px',
                    height: this.videoBoxSize.height + 'px',
                }
            },
            loadingStyle(){
                return {
                    width: this.videoBoxSize.width + 'px',
                    height: this.videoBoxSize.height + 'px',
                    'font-size': 'xx-large',
                    'line-height': this.videoBoxSize.height + 'px',
                    'text-align': 'center',
                }
            },
            ...Vuex.mapGetters([types.STATE_room_id, types.STATE_videoBoxSize]),
        },
        apollo: {
            room: {
                query: gql`query GetPlayerConfig($player_type: String!, $room_id: ID!){
                    room(room_id: $room_id){
                        playerConfig(player_type: $player_type){
                            ... on PlayerMpsConfig{
                                appId,
                                autostart,
                                controlbardisplay,
                                isclickplay,
                                isfullscreen,
                                mobilefullscreen,
                                player_type,
                                room_id,
                                stretching,
                                uin,
                            }
                            ... on PlayerAodianConfig{
                                adveDeAddr,
                                autostart,
                                bufferlength,
                                controlbardisplay,
                                defvolume,
                                hlsUrl,
                                maxbufferlength,
                                player_type,
                                room_id,
                                rtmpUrl,
                                stretching,
                            }
                        }
                    }
                }`,
                variables(){
                    return {
                        player_type: this.player_type,
                        room_id: this.room_id,
                    }
                },
                fetchPolicy: 'network-only',
                result({ data, loader, networkStatus }) {
                    //console.log("We got some result!", data, loader, networkStatus)
                    data && data.room && data.room.playerConfig && load_player(this, data.room.playerConfig)
                },
            }
        },
	}
</script>
