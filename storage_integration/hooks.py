from . import __version__ as app_version

app_name = "storage_integration"
app_title = "Storage Integration"
app_publisher = "Frappe Technologies"
app_description = "S3 Storage Integration for Frappe Cloud"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "developers@frappe.io"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/storage_integration/css/storage_integration.css"
# app_include_js = "/assets/storage_integration/js/storage_integration.js"

# include js, css files in header of web template
# web_include_css = "/assets/storage_integration/css/storage_integration.css"
# web_include_js = "/assets/storage_integration/js/storage_integration.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "storage_integration/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "storage_integration.utils.jinja_methods",
# 	"filters": "storage_integration.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "storage_integration.install.before_install"
# after_install = "storage_integration.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "storage_integration.uninstall.before_uninstall"
# after_uninstall = "storage_integration.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "storage_integration.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }
doc_events = {
	"File": {
		"after_insert": "storage_integration.controller.upload_to_s3",
		"on_trash": "storage_integration.controller.delete_from_s3",
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"storage_integration.tasks.all"
# 	],
# 	"daily": [
# 		"storage_integration.tasks.daily"
# 	],
# 	"hourly": [
# 		"storage_integration.tasks.hourly"
# 	],
# 	"weekly": [
# 		"storage_integration.tasks.weekly"
# 	],
# 	"monthly": [
# 		"storage_integration.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "storage_integration.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "storage_integration.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "storage_integration.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"storage_integration.auth.validate"
# ]

