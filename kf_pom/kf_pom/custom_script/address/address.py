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