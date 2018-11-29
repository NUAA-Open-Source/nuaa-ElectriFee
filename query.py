# -*- coding: utf-8 -*-
import requests
import re
import sys
import random
from bs4 import BeautifulSoup
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import pickle
import json
import yaml

class Utils(object):
	@staticmethod
	def getViewstate(text):
		bs = BeautifulSoup(text, "html.parser")
		return bs.find("input", {"id": "__VIEWSTATE"}).attrs['value']

	@staticmethod
	def requests_retry_session(
		retries=3,
		backoff_factor=0.3,
		status_forcelist=(500, 502, 504),
		session=None,
	):
		session = session or requests.Session()
		retry = Retry(
			total=retries,
			read=retries,
			connect=retries,
			backoff_factor=backoff_factor,
			status_forcelist=status_forcelist,
		)
		adapter = HTTPAdapter(max_retries=retry)
		session.mount('http://', adapter)
		session.mount('https://', adapter)
		return session

	@staticmethod
	def getFee(text):
		bs = BeautifulSoup(text, "html.parser")
		return bs.find("span",{"class": "number"}).text

	@staticmethod
	def getDescriptiveText(text):
		bs = BeautifulSoup(text, "html.parser")
		return bs.find("h6").text

class QueryFee(object):

	uri = 'http://222.192.89.21/sims3/default.aspx'
	proxy = None
	room_mapping = {}

	def __init__(self, filepath: str):
		if not isinstance(filepath, str):
			print('[!] No data specified!')
			sys.exit()
		'''
		with open(filepath, 'r') as stream:
			try:
				self.room_mapping = yaml.load(stream)
			except yaml.YAMLError as exc:
				print(exc)
		'''
		with open(filepath, 'rb') as f:
			try:
				self.room_mapping = pickle.load(f)
			except:
				print('[!] Error when reading file.')

	def _ProcessResult(self, res, data):
		return Utils.getDescriptiveText(res)

	def _RoomRequest(self, sess, query_data, target_data):
		new_data = dict(query_data)
		new_data['drfangjian'] = target_data['drfangjian']
		extra = {'radio': 'buyR', 'ImageButton1.x': '45', 'ImageButton1.y': '4'}
		new_data = {**new_data, **extra}
		response = sess.post(self.uri, data=new_data, proxies=self.proxy, timeout=2)
		# Here should be some differences
		return self._ProcessResult(response.text, target_data)

	def _FloorRequest(self, sess, query_data, target_data):
		new_data = dict(query_data)
		new_data['dr_ceng'] = target_data['dr_ceng']
		response = sess.post(self.uri, data=new_data, proxies=self.proxy, timeout=2)
		new_data['__VIEWSTATE'] = Utils.getViewstate(response.text)
		return self._RoomRequest(sess, new_data, target_data)

	def _BuildingRequest(self, sess, query_data, target_data):
		new_data = dict(query_data)
		new_data['drceng'] = target_data['drceng']
		response = sess.post(self.uri, data=new_data, proxies=self.proxy, timeout=2)
		new_data['__VIEWSTATE'] = Utils.getViewstate(response.text)
		return self._FloorRequest(sess, new_data, target_data)

	def _RegionRequest(self, sess, query_data, target_data):
		new_data = dict(query_data)
		new_data['DropDownList1'] = target_data['DropDownList1']
		response = sess.post(self.uri, data=new_data, proxies=self.proxy, timeout=2)
		new_data['__VIEWSTATE'] = Utils.getViewstate(response.text)
		return self._BuildingRequest(sess, new_data, target_data)

	def _CampusRequest(self, sess, query_data, target_data):
		new_data = dict(query_data)
		new_data['drlouming'] = target_data['drlouming']
		response = sess.post(self.uri, data=new_data, proxies=self.proxy, timeout=2)
		new_data['__VIEWSTATE'] = Utils.getViewstate(response.text)
		return self._RegionRequest(sess, new_data, target_data)

	def _InitRequest(self, target_data: dict):
		s = Utils.requests_retry_session(retries=3)
		response = s.post(self.uri, proxies=self.proxy, timeout=1)
		query_data = {}
		query_data['__VIEWSTATE'] = Utils.getViewstate(response.text)
		return self._CampusRequest(s, query_data, target_data)

	def _ExecuteRequest(self, target_data: dict):
		# This should be implemented by recursion, but I just don't want to for it's a little bit disgusting
		# I love copying code!
		return self._InitRequest(target_data)

	def ExecuteQuery(self, campus: int, building: int, public_dorm: int, private_dorm: int = None):
		query_item_extra = None
		try:
			query_item = self.room_mapping[campus][building][public_dorm]
			if private_dorm is not None:
				query_item_extra = self.room_mapping[campus][building][public_dorm][private_dorm]
		except:
			print('[!] Record not found in database! Does this dorm exist?')
			sys.exit(1)

		for key, item in query_item.items():
			if isinstance(key, int) or key.isdigit(): # Priv Dorm
				continue
			try:
				res = self._ExecuteRequest(item)
			except requests.exceptions.ProxyError as e:
				print('[!] Proxy failed.')
				sys.exit(1)
			except requests.exceptions.Timeout as e:
				print('[!] Timeout occurs. Remote server may not be responding.')
				sys.exit(1)
			except requests.exceptions.RequestException as e:
				print('[!] Internal Server Error.')
				sys.exit(1)
			# print(key + ':' + res)
			print(res)

		if query_item_extra is not None:
			for key, item in query_item_extra.items():
				if isinstance(key, int) or key.isdigit():
					continue
				try:
					res = self._ExecuteRequest(item)
				except requests.exceptions.ProxyError as e:
					print('[!] Proxy failed.')
					sys.exit(1)
				except requests.exceptions.Timeout as e:
					print('[!] Timeout occurs. Remote server may not be responding.')
					sys.exit(1)
				except requests.exceptions.RequestException as e:
					print('[!] Internal Server Error.')
					sys.exit(1)
				# print(key + ':' + res)
				print(res)


if __name__ == "__main__":
	q = QueryFee(sys.argv[1])
	arg_copy = sys.argv.copy()
	arg_copy.pop(1)
	arg_copy.pop(0)
	arg_copy = [int(x) for x in arg_copy]
	q.ExecuteQuery(*arg_copy)
