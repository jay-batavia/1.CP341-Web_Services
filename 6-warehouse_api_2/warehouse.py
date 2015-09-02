import abc
class Warehouse(metaclass = abc.ABCMeta):
	'''Abstract base class for warehouse implementations'''

	@abc.abstractmethod
	def updateItemQuantity(self, item_name, update):
		'''Add or remove a quantity for a particular item.'''
		return

	@abc.abstractmethod
	def updateInventory(self, update):
		'''For each item in the update dictionary, update its value'''
		return

	@abc.abstractmethod
	def getItemQuantity(self, *args):
		'''Retrieve the quantity of one or more items in the inventory'''
		return
		
	@abc.abstractmethod
	def getBondedItems(self, query_params):
		'''Retrieve the items whose inventory matches the restricted quantities.'''
		return

	@abc.abstractmethod
	def deleteItem(self, inventory_id):
		'''Remove the specified item from inventory'''
		return
		