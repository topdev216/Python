'''
Created by auto_sdk on 2016.03.06
'''
from top.api.base import RestApi
class VmarketEticketCardReverseRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.codemerchant_id = None
		self.consume_secial_num = None
		self.id_card = None
		self.order_id = None
		self.posid = None
		self.reverse_num = None
		self.token = None

	def getapiname(self):
		return 'taobao.vmarket.eticket.card.reverse'
