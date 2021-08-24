from __future__ import unicode_literals
from frappe.model.document import Document
import frappe
import json

def validate(doc,method=None):
	# Make Approvers comments on PO madatory for certain approvers
	if((doc.workflow_state == 'Rejected by Director Approver' )and 'Director Approver' in frappe.get_roles()) :
		if doc.	approver_comments == None or doc.approver_comments == '':
			frappe.throw("Approver's comments are mandatory")
		else:
			doc.add_comment('Comment', text=doc.approver_comments)
			doc.approver_comments = ''

	if((doc.workflow_state == 'Director Approver Approved' )and 'Director Approver' in frappe.get_roles()):
		if doc.approver_comments:
			doc.add_comment('Comment', text=doc.approver_comments)
			doc.approver_comments = ''

	if((doc.workflow_state == 'Vendor Approved' or doc.workflow_state == 'Rejected by Vendor')and 'Vendor' in frappe.get_roles()):
		if doc.approver_comments:
			doc.add_comment('Comment', text=doc.approver_comments)
			doc.approver_comments = ''

	# #Send mails to the user and approvers
	# #creating url for doctype to send in email
 #    url = frappe.utils.get_url()
 #    doctype_url = url + "/desk#Form/Purchase Order/"+doc.name
 #    team_email=frappe.db.get_value("Team",{'name':doc.team},"team_email")

 #    msg ="""Dear %s Team,<br><br>Purchase Order %s <br>Following are the details. <br>"""%(doc.team,doc.name)
 #    frappe.sendmail(recipients=team_email,subject="Purchase Order Status",content=msg)
