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
    var self = this;
    this.config = redis_config;
    this.client = redis.createClient(redis_config.port, redis_config.host, {
        auth_pass: redis_config.password
    });
    this.client.on('ready', function(){
        console.log('redis ready');
        self.client.subscribe(self.config.subscribe_key, function(err) {
            console.log("redis subscribe:", self.config.subscribe_key, err);
        });
    });
    this.client.on("error", function(err) {
        console.log("redis error:", err);
    });
}
RedisHandler.prototype.GetTopicExtMap = function(callback) {
    var self = this;
    this.client.hgetall(this.config.topic_key, function(err, res) {
        console.log("redis get topic_key:", err, res);
        !err && callback(res);
    });
}
RedisHandler.prototype.DisConnect = function() {
    console.log("redis end");
    this.client.end();
}


function DMS(job_api, ext_dict, pub_key, sub_key, cid){
    var host = "mqtt.dms.aodianyun.com"
    var self = this;
    if(cid == "" || cid == null){
        cid = 'mqttjs'+ Math.floor( Math.random()*1000) + (new Date().getTime());
    }
    this.cid = cid;
    this.pub_key = pub_key;
    this.sub_key = sub_key;
    this.job_api = job_api;
    this.ext_dict = ext_dict;
    this.client = null;
    this.topic_map ={};

    this.client = mqtt.createClient(1883, host, {username: this.pub_key,password: this.sub_key, clean:false, clientId:cid});
    this.client.on("reconnect", function(err, info) {  // dms 重连之后 自动重新关注当前需要的话题列表
        console.log("dms on reconnect:", err, info);
        self.runOnTopic(self.job_api, self.ext_dict);
    });
    this.client.on("offline", function(err, info) {
        console.log("dms on offline:", err, info);
    });
    this.client.on("connect", function(err, info) {
        console.log("dms on connect:", err, info);
    });
    this.client.on("error", function(err, info) {
        console.log("dms on error:", err, info);
    });
    this.client.on("close", function(err, info) {
        console.log("dms on close:", err, info);
    });
    this.client.on('message', function(topic, message, opts) {
        console.log("dms on message:", topic, message, opts);
    });
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
DMS.prototype.runOnTopic = function(job_api, ext_dict){
    var self = this;
    this.job_api = job_api;
    this.ext_dict = ext_dict;
    this.topic(topic_list, function(err, info) {
        console.log("dms subscribe back:", err, info);
    }, function(err, info) {
        console.log("dms unsubscribe back:", err, info);
    });
}

function App(config) {
    console.log("app init");
    this.childMap = {};
    this.processMap = {};
    this.config = config;
    this.redis = new RedisHandler(config.redis_config);
    this.stop = false;
    this.Start();
}
App.prototype.Start = function() {
    console.log("app start");
    var self = this;
    console.log("app load redis topic_key");
    this.redis.GetTopicExtMap(function(msg_list) {
        for(var idx in msg_list){
            var msg = msg_list[idx];
            var skey = msg['pub_key']+':'+msg['sub_key'];
            var dms = skey in self.processMap ? self.processMap[skey] : new DMS(msg['job_api'], msg['ext_dict'], msg['pub_key'], msg['sub_key'], msg['client_id']);
            dms.runOnTopic(msg['job_api'], msg['ext_dict']);
            self.processMap[skey] = dms;
        }
    });
    console.log("app on redis message");
    this.redis.client.on('message', function(key, msg_str) {
        var msg = JSON.parse(msg_str);
        var skey = msg['pub_key']+':'+msg['sub_key'];
        if( msg.cmd=='reload' ){
            var dms = skey in self.processMap ? self.processMap[skey] : new DMS(msg['job_api'], msg['ext_dict'], msg['pub_key'], msg['sub_key'], msg['client_id']);
            dms.runOnTopic(msg['job_api'], msg['ext_dict']);
            self.processMap[skey] = dms;
        } else if( msg.cmd=='remove' ){
            var dms = skey in self.processMap ? self.processMap[skey] : null;
            if( dms ){
                dms.disconnect();
                delete self.processMap[skey];
            }
        }
    });
}
App.prototype.Stop = function() {
    console.log("app stop");
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