'''
Created by auto_sdk on 2012.11.23
'''
from top.api.base import RestApi
class SellercenterRolesGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.nick = None

	def getapiname(self):
		return 'taobao.sellercenter.roles.get'
