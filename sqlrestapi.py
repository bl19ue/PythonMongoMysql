#!/usr/bin/python
# -*- coding: utf-8 -*-
import bottle
import json

import MySQLdb as mdb

from bottle import route, run, request, abort
import datetime


db = mdb.connect('localhost', 'root', '1234', 'logindb');



@route('/shoes',method='POST')
def post_document():
    data=request.body
    entity=json.load(data)
    print entity
    cursor=db.cursor()
    d=datetime.datetime.now()
    date=d.strftime("%d/%m/%y")
    sql="""INSERT INTO shoe(shoeId,shoeName,shoeQuantity,createdBy,createdAt) VALUES(%s,%s,%s,%s,%s)"""
    data=(entity['shoeId'],entity['shoeName'],entity['shoeQuantity'],entity['createdBy'],date)
    cursor.execute(sql,data)
    db.commit()
    return date

@route('/shoe/<shoeId>', method='GET')
def get_document(shoeId):
    print "shoeId = %s" % shoeId
    try:
            cur = db.cursor()
            cur.execute("SELECT * FROM shoe where shoeId=shoeId")
            rows = cur.fetchone()
            print rows
    except Exception, e:
                print ( "Error: %s" % str(e))
                
    return str(rows)


@route('/shoes',method='PUT')
def put_document():
    data=request.body
    entity=json.load(data)
    print entity
    cursor=db.cursor()
    d=datetime.datetime.now()
    date=d.strftime("%d/%m/%y")
    sql="""UPDATE shoe SET shoeId=%s, shoeName=%s, shoeQuantity=%s, createdBy=%s, createdAt=%s  where shoeId=%s"""
    data=(entity['shoeId'],entity['shoeName'],entity['shoeQuantity'],entity['createdBy'],date,entity['shoeId'])
    cursor.execute(sql,data)
    db.commit()
    return date   

@route('/shoes',method='DELETE')
def put_document():
    data=request.body
    entity=json.load(data)
    print entity
    cursor=db.cursor()
    
    sql="""DELETE FROM shoe where shoeId=%s"""
    data=(entity['shoeId'])
    cursor.execute(sql,data)
    db.commit()
    return "deleted"           

run(host='localhost', port=8080)
