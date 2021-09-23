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
		s_email = frappe.db.get_singles_dict("KF Email Settings")
		r_email = s_email["director_approver"]
		url = base_url_dev + "/purchase-order/" + doc.name
		pr_no = doc.items[0].material_request
		subject = """Purchase Order %s has been submitted for Approval by %s for PR %s"""%(doc.name,get_user_fullname(doc.modified_by),pr_no)
		msg = """Hello %s, <br> The Purchase Order %s has been submitted for your approval by %s for PR %s
		(Category: %s, Sub category: %s)
		<br>Link: %s <br><br>Thanks,<br>Knight Frank Procurement Team
		"""%(get_user_fullname(r_email),doc.name,get_user_fullname(doc.modified_by),pr_no,doc.category,doc.sub_category,url)
		if s_email["email_configuration"] == "1":
			frappe.sendmail(recipients=r_email,subject=subject,content=msg)

	if 'Director Approver' in frappe.get_roles() and doc.workflow_state == 'Director Approver Approved':
		s_email = frappe.db.get_singles_dict("KF Email Settings")
		r_email = s_email["procurement_approver"]
		vendor_email = frappe.db.get_value('Address',{'name': doc.supplier_address},['email_id'])
		cc_email = vendor_email
		pr_no = doc.items[0].material_request
		subject = """You are awarded Purchase Order %s for PR %s"""%(doc.name,pr_no)
		items = ""
		for item in doc.items:
			items = items + "+" + item.item_name

		url = base_url_dev + "/purchase-order/" + doc.name
		msg = """Hello %s, <br> You are awarded Purchase Order %s for PR %s (Category: %s, Sub category:%s)
		<br>
		Please login and acknowledge the PO to be able to download PDF copy of the PO.
		<br> Link: %s <br><br>Thanks,<br>Knight Frank Procurement Team
		"""%(get_user_fullname(vendor_email),doc.name,pr_no,doc.category,doc.sub_category,url)
		if s_email["email_configuration"] == "1":
			frappe.sendmail(recipients=r_email,cc=cc_email,subject=subject,content=msg)	

	if 'Director Approver' in frappe.get_roles() and doc.workflow_state == 'Rejected by Director Approver':
		s_email = frappe.db.get_singles_dict("KF Email Settings")
		r_email = s_email["procurement_approver"]
		comments = frappe.db.sql(''' 
			Select content from `tabComment` where reference_doctype='Purchase Order' 
			and reference_name=%s 
			and comment_type='comment'
			and owner = %s
			''',(doc.name,doc.modified_by),as_list=1)
		pr_no = doc.items[0].material_request
		url = base_url_dev + "/purchase-order/" + doc.name
		subject = """Purchase Order %s has been Rejected by %s for PR %s"""%(doc.name,get_user_fullname(doc.modified_by),pr_no)
		msg = """Hello %s, <br> The Purchase Order %s for PR %s (Category: %s, Sub category: %s) has been rejected by %s with the following comments : %s.
		<br>Link: %s <br><br>Thanks,<br>Knight Frank Procurement Team
		"""%(get_user_fullname(r_email),doc.name,pr_no,doc.category,doc.sub_category,get_user_fullname(doc.modified_by),comments[0][0],url)
		if s_email["email_configuration"] == "1":
			frappe.sendmail(recipients=r_email,subject=subject,content=msg)

	if 'Vendor' in frappe.get_roles() and doc.workflow_state == 'Vendor Approved':
		s_email = frappe.db.get_singles_dict("KF Email Settings")
		r_email = s_email["procurement_approver"]
		cc_email = s_email["director_approver"]
		pr_no = doc.items[0].material_request
		url = base_url_dev + "/purchase-order/" + doc.name
		subject = """ PO %s for PR %s  has been Acknowledged by %s"""%(doc.name,pr_no,get_user_fullname(doc.modified_by))
		msg = """Hello %s <br> The PO %s for PR %s (Category: %s, Sub category: %s) has been acknowledged by the supplier %s.
		<br>Link: %s<br><br>Thanks,<br>Knight Frank Procurement Team
		"""%(get_user_fullname(r_email),doc.name,pr_no,doc.category,doc.sub_category,get_user_fullname(doc.modified_by),url)
		if s_email["email_configuration"] == "1":
			frappe.sendmail(recipients=r_email,cc=cc_email,subject=subject,content=msg)	

	if 'Vendor' in frappe.get_roles() and doc.workflow_state == 'Rejected by Vendor':
		s_email = frappe.db.get_singles_dict("KF Email Settings")
		r_email = s_email["procurement_approver"]
		pr_no = doc.items[0].material_request
		url = base_url_dev + "/purchase-order/" + doc.name
		subject = """PO %s for PR %s (Category: %s, Sub category: %s) has been Rejected by %s 
		"""%(doc.name,pr_no,doc.category,doc.sub_category,get_user_fullname(doc.modified_by))
		msg = """Hello %s <br> PO %s for PR %s has been rejected by %s 
		<br>Link: %s<br><br>Thanks,<br>Knight Frank Procurement Team
				"""%(get_user_fullname(r_email),doc.name,pr_no,get_user_fullname(doc.modified_by),url)
		if s_email["email_configuration"] == "1":
			frappe.sendmail(recipients=r_email,subject=subject,content=msg)

	
def get_permission_query_conditions(doctype):
	
	if frappe.session.user == "Administrator":
		return ""

	if "Director Approver" in frappe.get_roles():

		names = frappe.db.sql("""select name from `tabPurchase Order` 
								where workflow_state not in ('Created by Procurement Approver')""")

		if names:
			names = ",".join("'" + i[0]+"'" for i in names)
			names = "(" + names + ")"

		if names:
			return """(`tabPurchase Order`.name in %s)"""%(names)

		if not names:
		#to return nothing
			return """(`tabPurchase Order`.name is NULL)"""


	if "Vendor" in frappe.get_roles():
		corresponding_address = frappe.get_value("Address",{"email_id":frappe.session.user},"name")
		names = frappe.db.sql("""select name from `tabPurchase Order` 
								where workflow_state in ('Director Approver Approved','Vendor Approved','Rejected by Vendor') and supplier_address = '{0}' """.format(corresponding_address))

		if names:
			names = ",".join("'" + i[0]+"'" for i in names)
			names = "(" + names + ")"

		if names:
			return """(`tabPurchase Order`.name in %s)"""%(names)

		if not names:
		#to return nothing
			return """(`tabPurchase Order`.name is NULL)"""

	#Requestor/Site Manager can see only the PO for MR created by himself
	if "Requestor/Site Manager" in frappe.get_roles():
		user = frappe.session.user
		names = frappe.db.sql("""select name from `tabPurchase Order` 
								where requestor_email=%s """,(user))

		if names:
			names = ",".join("'" + i[0]+"'" for i in names)
			names = "(" + names + ")"

		if names:
			return """(`tabPurchase Order`.name in %s)"""%(names)

		if not names:
		#to return nothing
			return """(`tabPurchase Order`.name is NULL)"""

	#Commercial Approver can see only the PO for MR created by himself
	if "Commercial Approver" in frappe.get_roles():
		user = frappe.session.user
		names = frappe.db.sql("""select name from `tabPurchase Order` 
								where commercial_approver=%s """,(user))

		if names:
			names = ",".join("'" + i[0]+"'" for i in names)
			names = "(" + names + ")"

		if names:
			return """(`tabPurchase Order`.name in %s)"""%(names)

		if not names:
		#to return nothing
			return """(`tabPurchase Order`.name is NULL)"""