from . import __version__ as app_version

app_name = "kf_pom"
app_title = "KF_POM"
app_publisher = "Indictranstech"
app_description = "KF"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "test@indictranstech.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/kf_pom/css/kf_pom.css"
# app_include_js = "/assets/kf_pom/js/kf_pom.js"

# include js, css files in header of web template
# web_include_css = "/assets/kf_pom/css/kf_pom.css"
# web_include_js = "/assets/kf_pom/js/kf_pom.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "kf_pom/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
doctype_js = {
			  "Item":"kf_pom/custom_script/item/item.js",
			  "Supplier":"kf_pom/custom_script/supplier/supplier.js",
			  "Material Request":"kf_pom/custom_script/material_request/material_request.js",
			  "Purchase Order":"kf_pom/custom_script/purchase_order/purchase_order.js",
			  "Address":"kf_pom/custom_script/address/address.js"
			}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

fixtures = ['Role','Workflow', 'Workflow State', 'Workflow Action','Custom Field','Translation','Property Setter','Print Format']

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

# Installation
# ------------

# before_install = "kf_pom.install.before_install"
# after_install = "kf_pom.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "kf_pom.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
permission_query_conditions = {
	"Material Request": "kf_pom.kf_pom.custom_script.material_request.material_request.get_permission_query_conditions",
}
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
	"Material Request": {
		"validate": "kf_pom.kf_pom.custom_script.material_request.material_request.validate"
	},
	"Purchase Order": {
		"validate": "kf_pom.kf_pom.custom_script.purchase_order.purchase_order.validate"
	}
}
# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"kf_pom.tasks.all"
# 	],
# 	"daily": [
# 		"kf_pom.tasks.daily"
# 	],
# 	"hourly": [
# 		"kf_pom.tasks.hourly"
# 	],
# 	"weekly": [
# 		"kf_pom.tasks.weekly"
# 	]
# 	"monthly": [
# 		"kf_pom.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "kf_pom.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "kf_pom.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "kf_pom.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"kf_pom.auth.validate"
# ]

