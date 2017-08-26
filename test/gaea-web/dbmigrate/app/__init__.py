# coding: utf-8
import os
import hashlib
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import graphene
import graphql
from flask_graphql import GraphQLView

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
from app import models

def md5key(pwd):
    def _md5_str(in_str):
        m2 = hashlib.md5()
        m2.update(in_str)
        return m2.hexdigest().lower()

    SECRET_KEY = app.config.get('PHP_CONFIG', {}).get('CRYPT_KEY', '')
    tmp = _md5_str(pwd)
    tmp = _md5_str( SECRET_KEY + tmp )
    return _md5_str( tmp + SECRET_KEY )

@app.route('/')
@app.route('/index')
def index():
    with open(os.path.join(os.getcwd(), 'GraphiQL.html'), 'r') as rf:
        return rf.read()


_schema = models.schema

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=_schema, graphiql=True))

if __name__ == '__main__':
    test_str = '''
query IntrospectionQuery { __schema { queryType { name } mutationType { name } subscriptionType { name } types { ...FullType } directives { name description locations args { ...InputValue } } } } fragment FullType on __Type { kind name description fields(includeDeprecated: true) { name description args { ...InputValue } type { ...TypeRef } isDeprecated deprecationReason } inputFields { ...InputValue } interfaces { ...TypeRef } enumValues(includeDeprecated: true) { name description isDeprecated deprecationReason } possibleTypes { ...TypeRef } } fragment InputValue on __InputValue { name description type { ...TypeRef } defaultValue } fragment TypeRef on __Type { kind name ofType { kind name ofType { kind name ofType { kind name } } } }
    '''
    test = _schema.execute(test_str)
    print 'data:', test.data
    print 'errors:', test.errors
