import frappe
from storage_integration.controller import MinioConnection


def get_context(context):
	# get backup urls from s3
	# create a download_backup function and download backup from
	files = frappe.get_all("Storage Backup", ["file_name", "key", "date"])

	return {"files": files}


@frappe.whitelist()
def create_backups():
	from frappe.utils.backups import backup

	backup_files = backup(with_files=False)
	path = backup_files["backup_path_db"]

	minio = MinioConnection(None)
	minio.upload_backup(path)
