from __future__ import unicode_literals
from frappe.model.document import Document
import frappe
import json
from frappe.utils.user import get_user_fullname

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

	# send the emails on creation,approval and rejection
	from frappe.utils import get_url	
	base_url_dev = get_url() + "/app" 
	if 'Procurement  Approver' in frappe.get_roles() and doc.workflow_state == 'Submitted by Procurement Approver':
		r_email = frappe.db.get_value('Has Role',{'role': 'Director Approver'},['parent'])
		url = base_url_dev + "/purchase-order/" + doc.name
		pr_no = doc.items[0].material_request
		subject = """Purchase Order %s has been submitted for Approval by %s for PR %s"""%(doc.name,get_user_fullname(doc.modified_by),pr_no)
		msg = """Hello %s, <br> The Purchase Order %s has been submitted for your approval by %s for PR %s.
		<br>Link: %s <br><br>Thanks,<br>Knight Frank Procurement Team
		"""%(get_user_fullname(r_email),doc.name,get_user_fullname(doc.modified_by),pr_no,url)
		frappe.sendmail(recipients=r_email,subject=subject,content=msg)

	if 'Director Approver' in frappe.get_roles() and doc.workflow_state == 'Director Approver Approved':
		r_email = frappe.db.get_value('Has Role',{'role': 'Procurement  Approver'},['parent'])
		vendor_email = frappe.db.get_value('Address',{'name': doc.supplier_address},['email_id'])
		cc_email = vendor_email
		subject = """You are awarded Purchase Order %s."""%(doc.name)
		pr_no = doc.items[0].material_request
		items = ""
		for item in doc.items:
			items = items + "+" + item.item_name

		url = base_url_dev + "/purchase-order/" + doc.name
		msg = """Hello %s, <br> You are awarded Purchase Order %s for %s.
		<br>
		Please login and acknowledge the PO to be able to download PDF copy of the PO.
		<br> Link: %s <br><br>Thanks,<br>Knight Frank Procurement Team
		"""%(get_user_fullname(vendor_email),doc.name,pr_no,url)
		frappe.sendmail(recipients=r_email,cc=cc_email,subject=subject,content=msg)	

	if 'Director Approver' in frappe.get_roles() and doc.workflow_state == 'Rejected by Director Approver':
		r_email = frappe.db.get_value('Has Role',{'role': 'Procurement  Approver'},['parent'])
		
		comments = frappe.db.sql(''' 
			Select content from `tabComment` where reference_doctype='Purchase Order' 
			and reference_name=%s 
			and comment_type='comment'
			and owner = %s
			''',(doc.name,doc.modified_by),as_list=1)

		url = base_url_dev + "/purchase-order/" + doc.name
		subject = """Purchase Order %s has been Rejected"""%(doc.name)
		msg = """Hello %s, <br> The Purchase Order %s has been rejected by %s with the following comments : %s.
		<br>Link: %s <br><br>Thanks,<br>Knight Frank Procurement Team
		"""%(get_user_fullname(r_email),doc.name,get_user_fullname(doc.modified_by),comments[0][0],url)
		frappe.sendmail(recipients=r_email,subject=subject,content=msg)	

	if 'Vendor' in frappe.get_roles() and doc.workflow_state == 'Vendor Approved':
		r_email = frappe.db.get_value('Has Role',{'role': 'Procurement  Approver'},['parent'])
		cc_email = frappe.db.get_value('Has Role',{'role': 'Director Approver'},['parent'])
		subject = """ PO Acknowledged %s by %s"""%(doc.name,get_user_fullname(doc.modified_by))
		msg = """Hello %s <br> The has been acknowledged by the supplier %s.
		<br><br>Thanks,<br>Knight Frank Procurement Team
		"""%(get_user_fullname(r_email),get_user_fullname(doc.modified_by))
		frappe.sendmail(recipients=r_email,cc=cc_email,subject=subject,content=msg)	

	if 'Vendor' in frappe.get_roles() and doc.workflow_state == 'Rejected by Vendor':
		r_email = frappe.db.get_value('Has Role',{'role': 'Procurement  Approver'},['parent'])
		subject = """PO Rejected %s by %s """%(doc.name,get_user_fullname(doc.modified_by))
		msg = """Hello %s <br> PO rejected %s by %s 
		<br><br>Thanks,<br>Knight Frank Procurement Team
				"""%(get_user_fullname(r_email),doc.name,get_user_fullname(doc.modified_by))
		frappe.sendmail(recipients=r_email,subject=subject,content=msg)	