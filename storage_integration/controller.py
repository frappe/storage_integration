# -*- coding: utf-8 -*-
import frappe
from frappe.utils.password import get_decrypted_password
import os
import re
from minio import Minio
from urllib.parse import urlparse, parse_qs


class MinioConnection:
	def __init__(self, doc):
		self.settings = frappe.get_doc("Storage Integration Settings", None)
		self.file = doc
		self.client = Minio(
			self.settings.ip,
			access_key=self.settings.access_key,
			secret_key=get_decrypted_password(
				"Storage Integration Settings", "Storage Integration Settings", "secret_key"
			),
			region=self.settings.region,
			secure=False,
		)

	def upload_file(self):
		if not self.file.is_folder:
			if re.search(r"\bhttps://\b", self.file.file_url):
				# if file already on s3
				return

			key, fkey = self.get_object_key()

			with open("./" + key, "rb") as f:
				self.client.put_object(
					self.settings.bucket_name, fkey, f, length=-1, part_size=10 * 1024 * 1024
				)

			method = "storage_integration.controller.download_from_s3"
			self.file.file_url = f"https://{frappe.local.site}/api/method/{method}?doc_name={self.file.name}&local_file_url={fkey}"

			os.remove("./" + key)
			self.file.save()
			frappe.db.commit()

	def upload_backup(self, path):
		with open(path, "rb") as f:
			self.client.fput_object(self.settings.bucket_name, path[2:], path)

		# on upload successful create storage_backup_doc()
		url = re.search(r"\bbackups/\b", path)

		doc = frappe.get_doc(
			{
				"doctype": "Storage Backup",
				"file_name": path[url.span()[1] :],
				"key": path[2:],
				"available": 1,
			}
		)

		doc.insert()
		os.remove(path)
		frappe.db.commit()

	def download_backup(self, file_name):
		key = frappe.local.site + "/private" + "/backups/" + file_name
		try:
			response = self.client.get_object(self.settings.bucket_name, key)
			frappe.local.response["filename"] = file_name
			frappe.local.response["filecontent"] = response.read()
			frappe.local.response["type"] = "download"
		finally:
			response.close()
			response.release_conn()

	def delete_file(self):
		key, fkey = self.get_object_key()
		self.client.remove_object(self.settings.bucket_name, fkey)

	def download_file(self, action_type):
		key, fkey = self.get_object_key()
		hash = self.file.content_hash
		file_new = append_id(hash, replace_umlauts(self.file.file_name))
		try:
			response = self.client.get_object(
				self.settings.bucket_name, fkey, file_new
			)
			if action_type == "download":
				frappe.local.response["filename"] = self.file.file_name
				frappe.local.response["filecontent"] = response.read()
				frappe.local.response["type"] = "download"
			elif action_type == "clone":
				with open("./" + key, "wb") as f:
					f.write(response.read())
			elif action_type == "restore":
				with open("./" + key, "wb") as f:
					f.write(response.read())

					if self.file.is_private:
						pattern = frappe.local.site
					else:
						pattern = "/public"

					match = re.search(rf"\b{pattern}\b", key)
					key = key[match.span()[1] :]
					self.file.file_url = key
					self.file.save()

			frappe.db.commit()
		finally:
			response.close()
			response.release_conn()

	def get_object_key(self):
		match = re.search(r"\bhttps://\b", self.file.file_url)
		url = frappe.db.get_value('File', self.file.name, 'file_url')
		hash = self.file.content_hash
		if match:
			query = urlparse(self.file.file_url).query
			self.file.file_url = parse_qs(query)["local_file_url"][0]

		if not self.file.is_private:
			key = frappe.local.site + "/public" + url
			fkey = frappe.local.site + "/public" + "/" + self.file.folder + "/" + append_id(hash, replace_umlauts(self.file.file_name))
		else:
			key = frappe.local.site + url
			fkey = frappe.local.site + "/" + self.file.folder + "/" + append_id(hash, replace_umlauts(self.file.file_name))

		return key, fkey
	
	def file_rename(self):
		key, fkey = self.get_object_key()
		hash = self.file.content_hash
		key_new = append_id(hash, replace_umlauts(key))
		url_new = file_new = append_id(hash, replace_umlauts(self.file.file_url))
		# file = frappe.get_doc("File", doc)
		# if not file.is_private:
		# 	key = frappe.local.site + "/public" + file.file_url
		# 	key_new = frappe.local.site + "/public" + replace_umlauts(file.file_url)
		# else:
		# 	key = frappe.local.site + file.file_url
		# 	key_new = frappe.local.site + replace_umlauts(file.file_url)

		os.rename("./" + key, "./" + key_new)
		frappe.db.set_value('File', self.file.name, 'file_url', url_new, update_modified=False)
		frappe.db.commit()
	
	# def read_file(self):
	# 	key, fkey = self.get_object_key()
	# 	response = self.client.get_object(
	# 		self.settings.bucket_name, fkey, self.file.file_name
	# 	)
	# 	return response


		


def upload_to_s3(doc, method):
	conn = MinioConnection(doc)
	conn.file_rename()
	conn.upload_file()


def delete_from_s3(doc, method):
	if doc.file_url.startswith("https://" + frappe.local.site + "/api/method/storage_integration"):
		conn = MinioConnection(doc)
		conn.delete_file()
	else:
		frappe.delete_doc("File", doc.name, ignore_on_trash=True)
		

@frappe.whitelist()
def download_from_s3(doc_name):
	doc = frappe.get_doc("File", doc_name)
	conn = MinioConnection(doc)
	conn.download_file(action_type="download")

@frappe.whitelist()
def read_from_s3(doc_name):
	doc = frappe.get_doc("File", doc_name)
	conn = MinioConnection(doc)
	conn.read_file()


@frappe.whitelist(allow_guest=True)
def download_backup(file_name):
	conn = MinioConnection(None)
	conn.download_backup(file_name)


@frappe.whitelist()
def migrate_existing_files():
	files = frappe.get_all("File", pluck="name", filters={"file_url": ("!=", "")})

	for file in files:
		doc = frappe.get_doc("File", file)
		upload_to_s3(doc, None)


@frappe.whitelist()
def delete_all_remote():
	files = frappe.get_all("File", pluck="name", filters={"file_url": ("!=", "")})

	for file in files:
		doc = frappe.get_doc("File", file)
		delete_from_s3(doc, None)


@frappe.whitelist()
def clone_files(action_type):
	files = frappe.get_all("File", pluck="name", filters={"file_url": ("!=", "")})

	for file in files:
		doc = frappe.get_doc("File", file)
		conn = MinioConnection(doc)
		conn.download_file(action_type=action_type)

def replace_umlauts(text:str) -> str:
	"""replace special German umlauts (vowel mutations) from text. 
	ä -> ae...
	ü -> ue 
	"""
	vowel_char_map = {ord('ä'):'ae', ord('ü'):'ue', ord('ö'):'oe', ord('ß'):'ss', ord('\u0308'):''}
	return text.translate(vowel_char_map)

def append_id(hash, filename):
	name, ext = os.path.splitext(filename)
	return "{name}_{uid}{ext}".format(name=name, uid=hash[:4], ext=ext)