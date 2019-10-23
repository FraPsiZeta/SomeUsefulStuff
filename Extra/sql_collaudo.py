import mysql.connector
from mysql.connector import Error
from collections import OrderedDict

class MySQL:
    def __init__(self):
        self.config_options = {
                            "user" : "collaudi_phdb",
                            "password" : "collaudi_phdb",
                            "host" : "dbsadel.sadel.it",
                            "database" : "phdb",
                            "charset" : "utf8",
                            "use_pure" : True
                        }

    def __connect(self):
        try:
            self.__connection = mysql.connector.connect(**(self.config_options))
            self.__cursor = self.__connection.cursor()
        except Error as err:
            printf("Errore nella connessione al server MySQL", err)

    def __close(self):
        self.__cursor.close()
        self.__connection.close()

    def generic_query(self, query):
        self.__connect()
        self.__cursor.execute(query)
        result = self.__cursor.fetchall()
        return result

    def select(self, table, *args, where=None, **kwargs):
        result = None
        query = 'SELECT '
        keys = args
        values = tuple(kwargs.values())
        l = len(keys) - 1

        for i, key in enumerate(keys):
            query += "`"+key+"` "
            if i < l:
                query += ","
        ## End for keys

        query += 'FROM %s' % table

        if where:
            query += " WHERE %s" % where
        ## End if where

        self.__connect()
        self.__cursor.execute(query, values)
        number_rows = self.__cursor.rowcount
        number_columns = len(self.__cursor.description)

        if number_rows >= 1 and number_columns > 1:
            result = [item for item in self.__cursor.fetchall()]
        else:
            result = [item[0] for item in self.__cursor.fetchall()]
        self.__close()

        return result
    ## End def select

    def update(self, table, *args, where=None, **kwargs):
        query  = "UPDATE %s SET " % table
        keys   = kwargs.keys()
        values = tuple(kwargs.values()) + tuple(args)
        l = len(keys) - 1
        for i, key in enumerate(keys):
            query += "`"+key+"` = %s"
            if i < l:
                query += ","
            ## End if i less than 1
        ## End for keys
        query += " WHERE %s" % where

        self.__connect()
        self.__cursor.execute(query, values)
        self.__connection.commit()

        # Obtain rows affected
        update_rows = self.__cursor.rowcount
        self.__close()

        return update_rows
    ## End function update

    def insert(self, table, *args, **kwargs):
        values = None
        query = "INSERT INTO %s " % table
        if kwargs:
            keys = kwargs.keys()
            values = tuple(kwargs.values())
            query += "(" + ",".join(["`%s`"] * len(keys)) %  tuple (keys) + ") VALUES (" + ",".join(["%s"]*len(values)) + ")"
        elif args:
            values = args
            query += " VALUES(" + ",".join(["%s"]*len(values)) + ")"

        self.__connect()
        self.__cursor.execute(query, values)
        self.__connection.commit()
        self.__close()
        return self.__cursor.lastrowid
    ## End def insert

    def delete(self, table, *args, where=None):
        query = "DELETE FROM %s" % table
        if where:
            query += ' WHERE %s' % where

        values = tuple(args)

        self.__connect()
        self.__cursor.execute(query, values)
        self.__connection.commit()

        # Obtain rows affected
        delete_rows = self.__cursor.rowcount
        self.__close()

        return delete_rows
    ## End def delete

    def select_advanced(self, sql, *args):
        od = OrderedDict(args)
        query  = sql
        values = tuple(od.values())
        self.__connect()
        self.__cursor.execute(query, values)
        number_rows = self.__cursor.rowcount
        number_columns = len(self.__cursor.description)

        if number_rows >= 1 and number_columns > 1:
            result = [item for item in self.__cursor.fetchall()]
        else:
            result = [item[0] for item in self.__cursor.fetchall()]

        self.__close()
        return result

    # try:
    #     connection = mysql.connector.connect(**config_options)
    #     cursor = connection.cursor()
    #     # cursor.execute("SHOW TABLES")
    #     cursor.execute("select * from COLLAUDI_HISTORY")
    #     records = cursor.fetchall()
    #     # print(cursor.fetchall())
    #     for row in records:
    #         print("Id = ", row[0], )
    #         print("Name = ", row[1])
    #         print("Price  = ", row[2])
    #         print("Purchase date  = ", row[3], "\n")
    # except Error as err:
    #     print("Errore nella lettura delle tabelle mySQL:", err)
    # finally:
    #     if (connection.is_connected()):
    #         connection.close()
    #         cursor.close()
    #         print("MySQL connection is closed")
    
