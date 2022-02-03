from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in storage_integration/__init__.py
from storage_integration import __version__ as version

setup(
	name="storage_integration",
	version=version,
	description="S3 Storage Integration for Frappe Cloud",
	author="Frappe Technologies",
	author_email="developers@frappe.io",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
