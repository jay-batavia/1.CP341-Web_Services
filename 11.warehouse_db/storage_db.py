import storage
import sqlite3



class StorageDB( storage.WarehouseStorage ):
    filename = 'warehouse_db_storage.sqlite'
    conn = None
    cur = None
    table = 'Items'

    def open( self ):
        try:
            self.conn = sqlite3.connect( self.filename )
            self.cur = self.conn.cursor()
        except:
            print( "Failed to open SQLite DB %s" % self.filename )
        self.cur.execute('CREATE TABLE IF NOT EXISTS Items(item text PRIMARY KEY, quantity int)')

    def close( self ):
        try:
            self.conn.commit()
            self.conn.close()
        except:
            print( "Failed to close SQLite DB %s" % self.filename )

    def updateQty(self, item_name, new_quantity):
        self.cur.execute('REPLACE INTO Items (item, quantity) VALUES(?, ?)', (item_name, new_quantity))


    def addItem( self, item_name, quantity ):
        # self.cur.execute( 'INSERT OR REPLACE INTO Items (name, qty) VALUES (%s, %d)' %
        #                   ( item_name, quantity ) )
        print("adding item")
        self.cur.execute( 'INSERT OR REPLACE INTO Items (item, quantity) VALUES (?, ?)',
                          ( item_name, quantity ) )

    def getItemQty( self, *args ):
        #name, prefix, limit, page
        name = args[0]
        prefix = args[1]
        limit = args[2]
        offset = args[3]*limit
        result = {}
        upper_bound = args[4]
        lower_bound = args[5]
        count = 0

        stmt = 'SELECT * FROM ' + self.table
        #Get specific quantity

        if len(name)>0:
            stmt = stmt + ' WHERE item = ?'
            self.cur.execute(stmt, (name,))
            count = 1
        #If there is a prefix query
        elif len(name) == 0 and len(prefix) > 0:
            stmt = stmt+ ' WHERE quantity >= ? AND quantity <= ?'
            stmt = stmt + ' AND WHERE item like ?'
            stmt = stmt + ' ORDER BY item ASC LIMIT ?'
            if(offset > 0):
                stmt = stmt + ' OFFSET ?'
                self.cur.execute(stmt, (lower_bound, upper_bound, str.lower(prefix)+"%", limit, offset))
            else:
                self.cur.execute(stmt, (lower_bound, upper_bound, str.lower(prefix)+"%", limit,))
        #Get full inventory
        elif len(name) == 0 and len(prefix) == 0:
            stmt = stmt + ' WHERE quantity >= ? AND quantity <= ?'
            stmt = stmt + ' ORDER BY item ASC LIMIT ?'
            if(offset > 0):
                stmt = stmt + ' OFFSET ?'
                self.cur.execute(stmt, (lower_bound, upper_bound, limit, offset))
            else:
                self.cur.execute(stmt, (lower_bound, upper_bound, limit,))
        else:
            print ("Something is wrong")

        result_list = self.cur.fetchall()
        result = dict(result_list)
        result['page_'] = offset
        result['total_pages'] = 'tbd'
       
        if result is None:
            return None
        else:
            return result

    def getTotalItems( self ):
        self.cur.execute('SELECT COUNT(*) FROM Items')
        number_items = self.cur.fetchone()[0]

        if number_items is None:
            return None
        else:
            return number_items


    def delItem( self, item_name ):
        results = self.cur.execute( 'DELETE FROM Items WHERE item = ?', ( item_name, ) )
        return results.rowcount > 0
