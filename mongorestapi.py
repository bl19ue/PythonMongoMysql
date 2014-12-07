import json
import bottle
import datetime
from bottle import route, run, request, abort
from pymongo import Connection

connection = Connection('localhost', 27017)
db = connection.mydb

@route('/shirt/<shirtId>', method='GET')
def get_document(shirtId):
    print "shirtId = %s" % shirtId
    try:
        entity = db['shirt'].find_one({'shirtId': shirtId})
    except Exception, e:
        print ( "Error: %s" % str(e))
        return null
    if not entity:
        abort(404, 'No documents with ShirtId %s' % shirtId)
    return str(entity)


@route('/shirts', method='POST')
def post_document():
    data = request.body.read()
    print "data = %s" % data
    if not data:
        abort(400, 'No data received')
    entity = json.loads(data)
    if not entity.has_key('shirtId'):
        abort(400, 'No _id specified')
    try:
        date = datetime.datetime.now()
        d = date.strftime("%d/%m/%y")
        print "date = %s" % d
        entity['createdAt'] = date
        db['shirt'].save(entity)
    except Exception, e:
        print ( "Error: %s" % str(e))
    return d


@route('/shirts', method='PUT')
def put_document():
    data = request.body.read()
    print "data = %s" % data
    if not data:
        abort(400, 'No data received')
    entity = json.loads(data)
    print "shirId = %s" % entity['shirtId']
    if not entity.has_key('shirtId'):
        abort(400, 'No _id specified')
    try:
        e = db['shirt'].find_one({'shirtId': entity['shirtId']})
        print "mongo data = %s" % e
        entity['_id'] = e['_id']
        db['shirt'].save(entity)
    except Exception, e:
        print ( "Error: %s" % str(e))
    return "OK"

@route('/shirts', method='DELETE')
def delete_document():
    data = request.body.read()
    print "data = %s" % data
    if not data:
        abort(400, 'No data received')
    entity = json.loads(data)
    print "shirId = %s" % entity['shirtId']
    if not entity.has_key('shirtId'):
        abort(400, 'No _id specified')
    try:
        e = db['shirt'].find_one({'shirtId': entity['shirtId']})
        print "mongo data = %s" % e
        entity['_id'] = e['_id']
        db['shirt'].remove(entity)
    except Exception, e:
        print ( "Error: %s" % str(e))
    return "Deleted"


run(host='localhost', port=8080)