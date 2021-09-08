# Copyright (c) 2021, Indictranstech and contributors
# For license information, please see license.txt

# import frappe

from __future__ import unicode_literals
from frappe.model.document import Document
import frappe
import json

class KFEmailSettings(Document):
	pass


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def user_query_for_PA(doctype,txt,searchfield, start, page_len, filters):
 	return frappe.db.sql("""
		select name from `tabUser` 
		where 
		name in (Select parent from `tabHas Role` 
					where parenttype='User' 
					and role = 'Procurement  Approver') 
					and enabled = 1
					and name like %(txt)s""".format(key=searchfield), {
        			'txt': "%{}%".format(txt)})

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def user_query_for_DA(doctype,txt,searchfield, start, page_len, filters):
 	return frappe.db.sql("""
		select name from `tabUser` 
		where 
		name in (Select parent from `tabHas Role` 
					where parenttype='User' 
					and role = 'Director Approver') 
					and enabled = 1
					and name like %(txt)s""".format(key=searchfield), {
        			'txt': "%{}%".format(txt)})