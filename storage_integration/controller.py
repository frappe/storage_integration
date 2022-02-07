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
			"localhost:9008",
			access_key=self.settings.access_key,
			secret_key=get_decrypted_password(
				"Storage Integration Settings", "Storage Integration Settings", "secret_key"
			),
			region=self.settings.region,
			secure=False,
		)

	def upload_file(self):
		if re.search(r"\bhttps://\b", self.file.file_url):
			# if file already on s3
			return

		key = self.get_object_key()
		with open("./" + key, "rb") as f:
			self.client.put_object(
				self.settings.bucket_name, key, f, length=-1, part_size=10 * 1024 * 1024
			)

		method = "storage_integration.controller.download_from_s3"
		self.file.file_url = f"https://{frappe.local.site}/api/method/{method}?doc_name={self.file.name}&local_file_url={self.file.file_url}"

		os.remove("./" + key)
		self.file.save()
		frappe.db.commit()

	def delete_file(self):
		obj_key = self.get_object_key()
		self.client.remove_object(self.settings.bucket_name, obj_key)

	def download_file(self, action_type):
		obj_key = self.get_object_key()

		try:
			response = self.client.get_object(
				self.settings.bucket_name, obj_key, self.file.file_name
			)
			if action_type == "download":
				frappe.local.response["filename"] = self.file.file_name
				frappe.local.response["filecontent"] = response.read()
				frappe.local.response["type"] = "download"
			elif action_type == "clone":
				with open("./" + obj_key, "wb") as f:
					f.write(response.read())
			elif action_type == "restore":
				with open("./" + obj_key, "wb") as f:
					f.write(response.read())

					if self.file.is_private:
						pattern = frappe.local.site
					else:
						pattern = "/public"

					match = re.search(rf"\b{pattern}\b", obj_key)
					obj_key = obj_key[match.span()[1] :]
					self.file.file_url = obj_key
					self.file.save()

			frappe.db.commit()
		finally:
			response.close()
			response.release_conn()

	def get_object_key(self):
		match = re.search(r"\bhttps://\b", self.file.file_url)

		if match:
			query = urlparse(self.file.file_url).query
			self.file.file_url = parse_qs(query)["local_file_url"][0]

		if not self.file.is_private:
			key = frappe.local.site + "/public" + self.file.file_url
		else:
			key = frappe.local.site + self.file.file_url

		return key


def upload_to_s3(doc, method):
	conn = MinioConnection(doc)
	conn.upload_file()


def delete_from_s3(doc, method):
	conn = MinioConnection(doc)
	conn.delete_file()


@frappe.whitelist()
def download_from_s3(doc_name):
	doc = frappe.get_doc("File", doc_name)
	conn = MinioConnection(doc)
	conn.download_file(action_type="download")


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
