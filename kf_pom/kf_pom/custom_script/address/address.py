from __future__ import unicode_literals
from frappe.model.document import Document
import frappe
import json

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def user_query(doctype,txt,searchfield, start, page_len, filters):
 	return frappe.db.sql("""
		select name from `tabUser` 
		where 
		name in (Select parent from `tabHas Role` 
					where parenttype='User' 
					and role = 'Commercial Approver') 
					and enabled = 1
					and name like %(txt)s""".format(key=searchfield), {
        			'txt': "%{}%".format(txt)})

def get_permission_query_conditions(user=None, doctype=None):
	if frappe.session.user == "Administrator":
		return ""
		
	if "Requestor/Site Manager" in frappe.get_roles():
		user = frappe.session.user
		names = frappe.db.sql("""select name from `tabAddress`  
								where name in (Select for_value from `tabUser Permission` 
								where allow ="Address" and user = %s)""",(user))

		if names:
			names = ",".join("'" + i[0]+"'" for i in names)
			names = "(" + names + ")"

		if names:
			return """(`tabAddress`.name in %s)"""%(names)

		if not names:
		#to return nothing
			return """(`tabAddress`.name is NULL)"""

	if "Commercial Approver" in frappe.get_roles():
		user = frappe.session.user
		names = frappe.db.sql("""select name from `tabAddress` 
								where commercial_approver=%s """,(user))

		if names:
			names = ",".join("'" + i[0]+"'" for i in names)
			names = "(" + names + ")"

		if names:
			return """(`tabAddress`.name in %s)"""%(names)

		if not names:
		#to return nothing
			return """(`tabAddress`.name is NULL)"""

	if "Vendor" in frappe.get_roles():
		user = frappe.session.user
		names = frappe.db.sql("""select name from `tabAddress` 
								where email_id=%s""",(user))

		if names:
			names = ",".join("'" + i[0]+"'" for i in names)
			names = "(" + names + ")"

		if names:
			return """(`tabAddress`.name in %s)"""%(names)

		if not names:
		#to return nothing
			return """(`tabAddress`.name is NULL)"""