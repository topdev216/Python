'''
Created by auto_sdk on 2015.07.21
'''
from top.api.base import RestApi
class VmarketEticketPackageExtendAddRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.package_extend = None

	def getapiname(self):
		return 'taobao.vmarket.eticket.package.extend.add'
