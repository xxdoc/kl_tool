var http = require('http');
var redis = require('redis');
var log4js = require("log4js");
var mqtt = require('mqtt')
var util = require("util");
var events = require("events");

var app_config = null;
if (process.argv.length > 2) {
    app_config = require(process.argv[2]);
} else {
    app_config = require("./config");
}
log4js.configure(app_config.log4js_config);
var logger = log4js.getLogger('normal');

function RedisHandler(redis_config) {
    console.log("redis config:", redis_config);
    this.config = redis_config;
    this.client = redis.createClient(redis_config.port, redis_config.host, {
        auth_pass: redis_config.password
    });
    this.client.on('ready', function(){
        console.log('redis ready');
    });
    this.client.on("error", function(err) {
        console.log("redis error:", err);
    });
}
RedisHandler.prototype.GetTopicList = function(skey, callback) {
    var self = this;
    this.client.hget(this.config.topic_key, skey,
    function(err, res) {
        console.log("redis get topic:", skey, res);
        callback(res);
    });
}
RedisHandler.prototype.DisConnect = function() {
    console.log("redis end");
    this.client.end();
}


function DMS(pub_key, sub_key, cid){
    var host = "mqtt.dms.aodianyun.com"
    this.client = null;
    this.topic_map ={};
    if(cid == "" || cid == null){
        cid = 'mqttjs'+ Math.floor( Math.random()*1000) + (new Date().getTime());
    }
    
    this.client = mqtt.createClient(1883, host, {username: pub_key,password: sub_key, clean:false, clientId:cid});
    this.client.on("reconnect", this.emit.bind(this, "reconnect"));
    this.client.on("offline", this.emit.bind(this, "offline"));
    this.client.on("connect", this.emit.bind(this, "connect"));
    this.client.on("error", this.emit.bind(this, "error"));
    this.client.on("close", this.emit.bind(this, "close"));
    this.client.on('message', this.emit.bind(this, "message"));
}
util.inherits(DMS, events.EventEmitter);
DMS.prototype.disconnect = function(){
    this.client.end();
}
DMS.prototype.publish=function(topic, msg, callback){
    var opt = {qos: 1, retain: false}
    this.client.publish(topic, msg, opt, callback);
}
DMS.prototype.subscribe = function(topic, callback){
    var map={}
    topic = (topic instanceof Array) ? topic : [topic, ];
    for(var k in topic){
        this.topic_map[topic[k]] = 1;
        map[topic[k]] = 1;
    }
    this.client.subscribe(map, callback);
}
DMS.prototype.unsubscribe = function(topic, callback){
    var map={}
    topic = (topic instanceof Array) ? topic : [topic, ];
    for(var k in topic){
        map[topic[k]] = 1;
        delete this.topic_map[topic[k]];
    }
    this.client.unsubscribe(map, callback);
}
DMS.prototype.topic = function(topic, sub_callback, unsub_callback){
    topic = (topic instanceof Array) ? topic : [topic, ];
    for(var item in this.topic_map){
        this.topic_map[item] = 0;
    }
    for(var k in topic){
        this.topic_map[topic[k]] = 1;
    }
    var sub_map = [],
        unsub_map = [];
    for(var item in this.topic_map){
        if( this.topic_map[item] == 1 ){
            sub_map.push(item);
        } else {
            unsub_map.push(item);
            delete this.topic_map[item];
        }
    }
    this.subscribe(sub_map, sub_callback);
    this.unsubscribe(unsub_map, unsub_callback);
}


function App(config) {
    console.log("App init");
    this.childMap = {};
    this.processMap = {};
    this.config = config;
    this.redis = new RedisHandler(config.redis_config);
    this.stop = false;
    this.Start();
}
App.prototype.Start = function() {
    console.log("App start");
    self = this;
    this.redis.subscribe(this.config.redis_config.subscribe_key);
    this.redis.on('message', function(key, msg_str) {
        var msg = JSON.parse(msg_str);
        var skey = msg['pub_key']+':'+msg['sub_key'];
        if( msg.cmd=='reload' ){
            dms = skey in self.processMap ? self.processMap[skey] : new DMS(msg['pub_key'], msg['sub_key']);
            self.redis.GetTopicList(skey , function(topic_list) {
                dms.topic(topic_list);
            })
            self.processMap[skey] = dms;
        } else if( msg.cmd=='remove' ){
            dms = skey in self.processMap ? self.processMap[skey] : null;
            if( dms ){
                dms.disconnect();
                delete self.processMap[skey];
            }
        }
    }
}
App.prototype.Stop = function() {
    console.log("App stop");
    this.stop = true;
    var exitMsg = {
        cmd: "exit"
    };
    for (var key in this.childMap) {
        this.childMap[key].send(exitMsg);
    };
}


var app = new App(app_config.config);

process.on('uncaughtException',
    function(err) {
        console.log('App exception: ', err, err.stack);
});