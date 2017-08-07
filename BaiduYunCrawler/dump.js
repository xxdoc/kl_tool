var c = db.yun.find({}, {'uk':1,'_id':0}).sort({"uk" : 1});
while(c.hasNext()) {
	print(c.next().uk+'');
}
