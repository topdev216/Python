#!/usr/bin/env python
# encoding: utf-8

import pymysql

class SimpleMySQL2:
    conn = None
    cur = None
    conf = None

    def __init__(self, **kwargs):
        self.conf = kwargs
        self.conf["keep_alive"] = kwargs.get("keep_alive", False) # add default values
        self.conf["charset"] = kwargs.get("charset", "utf8")
        self.conf["host"] = kwargs.get("host", "localhost")
        self.conf["port"] = kwargs.get("port", 3306)
        self.conf["autocommit"] = kwargs.get("autocommit", True) # change to automatically commit
        self.connect()

    def connect(self):
        try:
            self.conn = pymysql.connect(db=self.conf['db'], host=self.conf['host'],
                                        port=self.conf['port'], user=self.conf['user'],
                                        passwd=self.conf['passwd'],
                                        charset=self.conf['charset'])
            self.cur = self.conn.cursor(pymysql.cursors.DictCursor) # change to dict cursor
            self.conn.autocommit(self.conf["autocommit"])
        except:
            print("MySQL connection failed")
            raise

    def get_one(self, table=None, fields='*', where=None, order=None, limit=(0, 1)):
        return self._select(table, fields, where, order, limit).fetchone()

    def get_all(self, table=None, fields='*', where=None, order=None, limit=None):
        return self._select(table, fields, where, order, limit).fetchall()

    def left_join(self, tables=(), fields=(), join_fields=(), where=None, order=None, limit=None):
        return self._select_join(tables, fields, join_fields, where, order, limit).fetchall()

    def insert(self, table, data):
        query = self._serialize_insert(data)
        sql = "INSERT INTO %s (%s) VALUES(%s)" % (table, query[0], query[1])
        return self.query(sql, data.values()).rowcount

    def update(self, table, data, where=None):
        query = self._serialize_update(data)
        sql = "UPDATE %s SET %s" % (table, query)
        if where and len(where) > 0:
            sql += " WHERE %s" % where[0]
        return self.query(sql, list(data.values()) + list(where[1]) if where and len(where) > 1 else list(data.values())).rowcount

    def insert_update(self, table, data, keys):
        insert_data = data.copy()
        data = {k: data[k] for k in data if k not in keys}
        insert = self._serialize_insert(insert_data)
        update = self._serialize_update(data)
        sql = "INSERT INTO %s (%s) VALUES(%s) ON DUPLICATE KEY UPDATE %s" % (table, insert[0], insert[1], update)
        return self.query(sql, list(insert_data.values()) + list(data.values()) ).rowcount

    def delete(self, table, where=None):
        sql = "DELETE FROM %s" % table
        if where and len(where) > 0:
            sql += " WHERE %s" % where[0]
        return self.query(sql, where[1] if where and len(where) > 1 else None).rowcount

    def query(self, sql, params=None):
        try:
            self.cur.execute(sql, params)
        except:
            print("Query failed")
            raise
        return self.cur

    def commit(self):
        return self.conn.commit()

    def is_open(self):
        return self.conn.open

    def end(self):
        if self.cur: self.cur.close()
        if self.conn: self.conn.close()

    def _serialize_insert(self, data):
        keys = ", ".join( data.keys() )
        vals = ", ".join(["%s" for k in data])
        return [keys, vals]

    def _serialize_update(self, data):
        return "=%s, ".join( data.keys() ) + "=%s"

    def _select(self, table=None, fields=(), where=None, order=None, limit=None):
        sql = "SELECT %s FROM `%s`" % (",".join(fields), table)
        if where and len(where) > 0:
            sql += " WHERE %s" % where[0]
        if order:
            sql += " ORDER BY %s" % order[0]
            if len(order) > 1:
                sql+= " %s" % order[1]
        if limit:
            sql += " LIMIT %s" % limit[0]
            if len(limit) > 1:
                sql+= ", %s" % limit[1]
        return self.query(sql, where[1] if where and len(where) > 1 else None)

    def _select_join(self, tables=(), fields=(), join_fields=(), where=None, order=None, limit=None):
        fields = [tables[0] + "." + f for f in fields[0]] + [tables[1] + "." + f for f in fields[1]]
        sql = "SELECT %s FROM %s LEFT JOIN %s ON (%s = %s)" % (",".join(fields), tables[0], tables[1],
            tables[0] + "." + join_fields[0], tables[1] + "." + join_fields[1])
        if where and len(where) > 0:
            sql += " WHERE %s" % where[0]
        if order:
            sql += " ORDER BY %s" % order[0]
            if len(order) > 1:
                sql += " " + order[1]
        if limit:
            sql += " LIMIT %s" % limit[0]
            if len(limit) > 1:
                sql += ", %s" % limit[1]
        return self.query(sql, where[1] if where and len(where) > 1 else None)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.end()
