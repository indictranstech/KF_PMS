from __future__ import unicode_literals
from frappe.model.document import Document
import frappe
import json

def validate(doc,method=None):
	
	if((doc.workflow_state == 'Commercial Approver Approved' or doc.workflow_state ==  'Rejected by Commercial Approver' )and 'Commercial Approver' in frappe.get_roles()) :
		if doc.	approver_comments == None or doc.approver_comments == '':
			frappe.throw("Approver's comments are mandatory")
		else:
			doc.add_comment('Comment', text=doc.approver_comments)
			doc.approver_comments = ''

	if(doc.workflow_state == 'Rejected by Procurement Approver' and 'Procurement  Approver' in frappe.get_roles()):
		if doc.	approver_comments == None or doc.approver_comments == '':
			frappe.throw("Approver's comments are mandatory")
		else:
			doc.add_comment('Comment', text=doc.approver_comments)
			doc.approver_comments = ''

	if(doc.workflow_state == 'Procurement Approver Approved' and 'Procurement  Approver' in frappe.get_roles()):
		if doc.approver_comments:
			doc.add_comment('Comment', text=doc.approver_comments)
			doc.approver_comments = ''