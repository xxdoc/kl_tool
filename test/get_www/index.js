
use www
db.link.drop()
db.link.count()
db.link.ensureIndex({"url":1},{"unique":true})
db.link.ensureIndex({"url":-1})
db.link.ensureIndex({"deep":1})
db.link.ensureIndex({"deep":-1})
db.link.ensureIndex({"do_flag":1})
db.link.ensureIndex({"do_flag":-1})
db.link.ensureIndex({"title":1})
db.link.ensureIndex({"description":1})
db.link.ensureIndex({"keywords":1})

db.link.dropIndex({"title":1})
db.link.dropIndex({"description":1})
db.link.dropIndex({"keywords":1})

db.link.getIndexes()






use html
db.html.ensureIndex({"url":1},{"unique":true})
db.html.getIndexes()




use soup
db.soup.ensureIndex({"url":1},{"unique":true})
db.soup.getIndexes()

