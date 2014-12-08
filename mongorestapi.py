import json
import bottle
import datetime
from bottle import route, run, request, abort
from pymongo import Connection
import MySQLdb as mdb

connection = Connection('localhost', 27017)
db = connection.mydb

db1 = mdb.connect('localhost', 'root', '1234', 'logindb');


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

#Start of Mysql python API
@route('/shoes',method='POST')
def post_document():
    data=request.body
    entity=json.load(data)
    print entity
    cursor=db1.cursor()
    d=datetime.datetime.now()
    date=d.strftime("%d/%m/%y")
    sql="""INSERT INTO shoe(shoeId,shoeName,shoeQuantity,createdBy,createdAt) VALUES(%s,%s,%s,%s,%s)"""
    data=(entity['shoeId'],entity['shoeName'],entity['shoeQuantity'],entity['createdBy'],date)
    cursor.execute(sql,data)
    db1.commit()
    return date

@route('/shoe/<shoeId>', method='GET')
def get_document(shoeId):
    print "shoeId = %s" % shoeId
    try:
	    rows = "";
            cur = db1.cursor()
            cur.execute("SELECT * FROM shoe where shoeId=%s" %shoeId)
            rows = cur.fetchone()
    except Exception, e:
            print ( "Error: %s" % str(e))
    return str(rows)


@route('/shoes',method='PUT')
def put_document():
    data=request.body
    entity=json.load(data)
    print entity
    cursor=db1.cursor()
    d=datetime.datetime.now()
    date=d.strftime("%d/%m/%y")
    sql="""UPDATE shoe SET shoeId=%s, shoeName=%s, shoeQuantity=%s, createdBy=%s, createdAt=%s  where shoeId=%s"""
    data=(entity['shoeId'],entity['shoeName'],entity['shoeQuantity'],entity['createdBy'],date,entity['shoeId'])
    cursor.execute(sql,data)
    db1.commit()
    return date

@route('/shoes',method='DELETE')
def put_document():
    data=request.body
    entity=json.load(data)
    print entity
    cursor=db1.cursor()

    sql="""DELETE FROM shoe where shoeId=%s"""
    data=(entity['shoeId'])
    cursor.execute(sql,data)
    db1.commit()
    return "deleted"


run(host='0.0.0.0', port=8080)
