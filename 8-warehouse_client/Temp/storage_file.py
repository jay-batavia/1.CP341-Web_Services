import storage
import json

filename = 'warehouse_file_storage.json'

class StorageFile( storage.WarehouseStorage ):
    items = {}

    def open( self ):
        try:
            f = open( filename )
            self.items = json.loads( f.read() )
        except:
            self.items = {}

    def close( self ):
        try:
            f = open( filename, 'w' )
            f.write( json.dumps( self.items ) )
        except:
            print( "Failed to write to file %s" % filename )

    def addItem( self, item_name, quantity ):
        self.items[ item_name ] = quantity

    def getItemQty( self, *args ):
        item_name = args[0]
        if len(item_name) == 0:
            return self.items
        else:
            if item_name in self.items:
                return {item_name: self.items[ item_name ]}

    def updateQty( self, item_name, new_quantity ):
        if item_name in self.items:
            self.items[item_name] = new_quantity

    def getBoundedItems(self, upper_bound, lower_bound ):
        bounded_items = {}
        for item in self.items:
            if self.items[item] <= upper_bound and self.items[item] >= lower_bound:
                bounded_items[item] = self.items[item]
            else:
                pass
        if len(bounded_items) == 0:
            return None
        
        return bounded_items

    def getPrefixItems(self, pattern):
        prefix_items = {}
        for key in self.items.keys():
            if key.startswith( pattern ):
                prefix_items[key] = self.items[key]
        if len(prefix_items) == 0:
            return None

        return prefix_items

    def getTotalItems( self ):
        total = 0
        for k, v in self.items.items():
            try:
                total += int(v)
            except:
                total = -1

        return total


    def delItem( self, item_name ):
        if item_name in self.items:
            del self.items[ item_name ]
            return true
        else:
            return false