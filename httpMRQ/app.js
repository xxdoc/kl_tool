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
            if( err ){
                console.log("redis subscribe error:", err);
            }
            console.log("redis subscribe:", self.config.subscribe_key);
        });
    });
    this.client.on("error", function(err) {
        console.log("redis error:", err);
    });
}
RedisHandler.prototype.GetTopicExtMap = function(callback) {
    var self = this;
    this.client.hgetall(this.config.topic_key, function(err, res) {
        if( err ){
            console.log("redis get topic_key error:", err);
        }
        console.log("redis get topic_key:", res);
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

    this.client = mqtt.connect('mqtt://mqtt.dms.aodianyun.com:1883', {username: this.pub_key,password: this.sub_key, clean:false, clientId:cid});
    this.client.on("reconnect", function(err, info) {  // dms 重连之后 自动重新关注当前需要的话题列表
        console.log("dms on reconnect:", err, info);
        self.runOnTopic(self.job_api, self.ext_dict);
    });
    this.client.on("offline", function(err, info) {
        console.log("dms on offline:", err, info);
    });
    this.client.on("connect", function(packet) {
        console.log("dms on connect:", packet);
    });
    this.client.on("error", function(err, info) {
        console.log("dms on error:", err, info);
    });
    this.client.on("close", function(err, info) {
        console.log("dms on close:", err, info);
    });
    this.client.on('message', function(topic, message, opts) {
        console.log("dms on message:", topic);
        var url_list = self.listJobUrl(topic, message);
        for(var idx in url_list){
            var url = url_list[idx];
            self.httpRequest(url, true);
        }
    });
}
DMS.prototype.httpRequest = function(url, is_log) {
    http.get(url, function(res) { 
        var res_str = "";
        res.on("data", function(data) {
            res_str += data;
        });
        res.on("end", function() {
            is_log && console.log("dms job request:", url, res.statusCode, res_str);
        });
    }).on('error', function(e) { 
        is_log && console.log("dms job error: ", url, e.message); 
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

DMS.prototype.listJobUrl = function(topic, message){
    if ( !(topic in this.ext_dict) ){
        return [];
    }
    var url_list = [];
    var ext_set = this.ext_dict[topic];
    for(var idx in ext_set){
        var ext_tmp = ext_set[idx];
        var queue = '';
        var tmp_idx = ext_tmp.indexOf('@');
        var task = ext_tmp.slice(0, tmp_idx);
        var ext = ext_tmp.slice(tmp_idx + 1);
        tmp_idx = task.indexOf('#');
        if( tmp_idx>0 ){
            queue = task.slice(tmp_idx + 1);
            task = task.slice(0, tmp_idx);
        }
        var query = '?queue=' + queue + '&topic=' + topic + '&message=' + message + '&ext=' + ext;
        var job_api = this.job_api.replace('{{task}}', task);
        
        url_list.push( job_api + encodeURI(query) );
    }
    return url_list;
}
DMS.prototype.subscribe = function(topic, callback){
    var tmp_list = [];
    topic = (topic instanceof Array) ? topic : [topic, ];
    for(var k in topic){
        this.topic_map[topic[k]] = 1;
        tmp_list.push( topic[k] );
    }
    console.log("dms subscribe:", tmp_list);
    tmp_list.length && this.client.subscribe(tmp_list, callback);
}
DMS.prototype.unsubscribe = function(topic, callback){
    var tmp_list = [];
    topic = (topic instanceof Array) ? topic : [topic, ];
    for(var k in topic){
        tmp_list.push( topic[k] );
        delete this.topic_map[topic[k]];
    }
    console.log("dms unsubscribe:", tmp_list);
    tmp_list.length && this.client.unsubscribe(tmp_list, callback);
}
DMS.prototype.topic = function(topic, sub_callback, unsub_callback){
    topic = (topic instanceof Array) ? topic : [topic, ];
    console.log("dms topic topic_map input:", topic, this.topic_map);

    var tmp_map = {};
    for(var item in this.topic_map){
        tmp_map[item] = 0;
    }
    for(var k in topic){
        tmp_map[topic[k]] = 1;
    }
    var sub_map = [],
        unsub_map = [];
    for(var item in tmp_map){
        if( tmp_map[item]==1 && this.topic_map[item]!=1 ){
            sub_map.push(item);
            this.topic_map[item] = 1;
        } else if( tmp_map[item]==0) {
            unsub_map.push(item);
            delete this.topic_map[item];
        }
    }
    console.log("dms topic topic_map out:", sub_map, unsub_map, this.topic_map);
    this.subscribe(sub_map, sub_callback);
    this.unsubscribe(unsub_map, unsub_callback);
}
DMS.prototype.runOnTopic = function(job_api, ext_dict){
    console.log("dms runOnTopic:", job_api, ext_dict);
    var self = this;
    this.job_api = job_api;
    this.ext_dict = ext_dict;
    var topic_list = [];
    for(var topic in this.ext_dict){
        topic_list.push(topic);
    }
    this.topic(topic_list, function(err, info) {
        if( err ){
            console.log("dms subscribe back error:", err);
        }
        console.log("dms subscribe back:", info);
    }, function(err, info) {
        if( err ){
            console.log("dms unsubscribe back error:", err);
        }
        console.log("dms unsubscribe back:", info);
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
            var msg = JSON.parse( msg_list[idx] );
            var skey = msg['pub_key']+':'+msg['sub_key'];
            var dms = skey in self.processMap ? self.processMap[skey] : new DMS(msg['job_api'], msg['ext_dict'], msg['pub_key'], msg['sub_key'], msg['client_id']);
            dms.runOnTopic(msg['job_api'], msg['ext_dict']);
            self.processMap[skey] = dms;
        }
    });
    console.log("app on redis message");
    this.redis.client.on('message', function(key, msg_str) {
        console.log("redis on message:", key, msg_str);
        if( key!=self.redis.config.subscribe_key ){
            return ;
        }
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