'''
Created by auto_sdk on 2012.11.29
'''
from top.api.base import RestApi
class FenxiaoGradeAddRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.name = None

	def getapiname(self):
		return 'taobao.fenxiao.grade.add'
