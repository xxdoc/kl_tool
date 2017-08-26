db.yun.find().forEach(function(x){var y={};y._id=x.uk;y.uname=x.uname;db.getinfo.insert(y);})

use baidu
db.yun.ensureIndex({"topic":1})
db.yun.getIndexes()
db.share.getIndexes()
db.yun.find({'uk':0})
db.yun.find({'uk':2})
db.yun.find({}, {'uk':1,'_id':0}).sort({"uk" : 1}).limit(1)




var c = db.yun.find({}, {'uk':1,'_id':0}).sort({"uk" : 1});
var tmp = null;
print('[');
while(c.hasNext()) {
	tmp = c.next();
	tmp.uk = tmp.uk.toString();
	printjson(tmp);
	print(',');
}
print(']');

mongo 127.0.0.1:27017/baidu dump.js > feed.json