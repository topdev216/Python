'''
Created by auto_sdk on 2015.01.23
'''
from top.api.base import RestApi
class TmallItemSizemappingTemplateCreateRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.template_content = None
		self.template_name = None

	def getapiname(self):
		return 'tmall.item.sizemapping.template.create'
