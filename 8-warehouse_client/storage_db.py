import storage
import sqlite3

filename = 'warehouse_db_storage.sqlite'

class StorageDB( storage.WarehouseStorage ):
    conn = None
    cur = None

    def open( self ):
        try:
            self.conn = sqlite3.connect( filename )
            self.cur = self.conn.cursor()
        except:
            print( "Failed to open SQLite DB %s" % filename )

    def close( self ):
        try:
            self.conn.commit()
            self.conn.close()
        except:
            print( "Failed to close SQLite DB %s" % filename )

    def updateQty(self, item_name, new_quantity):
        print(item_name, new_quantity)
        self.cur.execute('REPLACE INTO Items (item, quantity) VALUES(?, ?)', (item_name, new_quantity))


    def addItem( self, item_name, quantity ):
        # self.cur.execute( 'INSERT OR REPLACE INTO Items (name, qty) VALUES (%s, %d)' %
        #                   ( item_name, quantity ) )
        self.cur.execute( 'INSERT OR REPLACE INTO Items (item, quantity) VALUES (?, ?)',
                          ( item_name, quantity ) )

    def getItemQty( self, args ):
        if len(args) == 1:
            item_name = str.lower(args[0])
            results = self.cur.execute( 'SELECT * FROM Items WHERE item = ?', ( item_name, ) )
            result = results.fetchone()
        elif(len(args)==0):
            results = self.cur.execute('SELECT * FROM Items')
            result = results.fetchall()

        if type(result) == tuple:
            result_dict = {result[0]: result[1]}
        elif type(result) == list:
            result_dict = dict(result)   
    
        if result is None:
            return None
        else:
            return result_dict

    def getBoundedItems( self, upper_bound, lower_bound ):
        results = self.cur.execute('SELECT * FROM Items WHERE quantity >= ? and quantity <= ?', (lower_bound, upper_bound))
        result = results.fetchall()

        if result is None:
            return None
        else:
            return result


    def delItem( self, item_name ):
        results = self.cur.execute( 'DELETE FROM Items WHERE item = ?', ( item_name, ) )
        return results.rowcount > 0
