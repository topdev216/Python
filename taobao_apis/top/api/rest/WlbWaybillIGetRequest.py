'''
Created by auto_sdk on 2016.03.24
'''
from top.api.base import RestApi
class WlbWaybillIGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.waybill_apply_new_request = None

	def getapiname(self):
		return 'taobao.wlb.waybill.i.get'
