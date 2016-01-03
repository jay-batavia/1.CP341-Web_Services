
import abc

class WarehouseStorage( metaclass = abc.ABCMeta ):
    """abstract base class for warehouse storage implementations"""

    @abc.abstractmethod
    def open( self ):
        """Opens the storage implementation of choice"""
        return

    @abc.abstractmethod
    def close( self ):
        """Closes database or file being used for storage"""
        return

    @abc.abstractmethod
    def addItem( self, item_name, quantity ):
        """Adds the given item and its quantity to inventory"""
        return

    @abc.abstractmethod
    def getItemQty( self, item_name ):
        """Get the quantity for a specific item in the inventory"""
        return

    @abc.abstractmethod
    def getPrefixItems( self, pattern ):
        """Get the items whose names start with a given prefix"""
        return

    @abc.abstractmethod
    def getTotalItems ( self ):
        """Get the total number items in the inventory"""
        return

    @abc.abstractmethod
    def delItem( self, item_name ):
        """Delete the given item from inventory"""
        return

    @abc.abstractmethod
    def getBoundedItems(self, upper_bound, lower_bound):
        """Retrieves the items from inventory whose quantities match the given quantity restrictions"""
        return

    @abc.abstractmethod
    def updateQty(self, item_name, new_quantity):
        """Updates the item quantity by removing or adding the given quantity"""
        return
     