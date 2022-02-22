# -*- coding: utf-8 -*-
from math import fabs
import KBEngine
import GlobalConst
from KBEDebug import *

		
class LUA_TABLE:
	def __init__(self):
		pass

	def createObjFromDict(self, dct):
		contain = {}
		dictOrlist = dct["dictOrlist"] #ture是dict
		keys = dct["keys"] 
		values = dct["values"]
		if dictOrlist:
			contain = {}
			for k, v in zip(keys, values):
				contain[k] = v
		else:
			contain = list(values)
		return contain

	def getDictFromObj(self, obj):
		ans = {"dictOrlist" : True, "keys" : [], "values" : []}
		if isinstance(obj, dict):
			for k, v in obj.items():
				ans["keys"].append(k)
				ans["values"].append(v)
		elif isinstance(obj, list):
			ans["dictOrlist"] = False
			ans["values"] = obj
		else:
			assert(False, type(obj))
		return ans

	def isSameType(self, obj):
		return isinstance(obj, list) or isinstance(obj, dict)
