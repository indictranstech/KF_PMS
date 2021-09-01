from __future__ import unicode_literals
from frappe.model.document import Document
import frappe
import json
from frappe.utils.user import get_user_fullname

def validate(doc,method=None):
	if(doc.commercial_approver == None or doc.commercial_approver == ''):
		frappe.throw("Please get the commercial_approver mapped to the customer before creating the Purchase requisition for this customer")

	# validations for comments to be added by approvers
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

	from frappe.utils import get_url	
	base_url_dev = get_url() + "/app" 

	# send the emails on creation,approval and rejection
	if 'Requestor/Site Manager' in frappe.get_roles() and doc.workflow_state == 'Submitted by Requestor':
		r_email = doc.commercial_approver
		cc_email = doc.requestor_email
		url = base_url_dev + "/material-request/" + doc.name
		subject = """Purchase Requisition %s for %s has been submitted for your Approval by %s """%(doc.name,doc.kf_customer,doc.requestor_name)
		msg = """Hello %s, <br> The Purchase Requisition %s (Category: %s, Sub category: %s) for %s has been submitted for your approval by %s
		<br> Link : %s <br><br>Thanks,<br>Knight Frank Procurement Team
		"""%(get_user_fullname(r_email),doc.name,doc.category,doc.sub_category,doc.kf_customer,doc.requestor_name,url)
		frappe.sendmail(recipients=r_email,cc=cc_email,subject= subject,content=msg)

	if 'Commercial Approver' in frappe.get_roles() and doc.workflow_state == 'Commercial Approver Approved':
		r_email = frappe.db.get_value('Has Role',{'role': 'Procurement  Approver'},['parent'])
		cc_email = doc.requestor_email 
		url = base_url_dev + "/material-request/" + doc.name
		subject = """Purchase Requisition %s for %s has been submitted for your Approval by %s"""%(doc.name,doc.kf_customer,get_user_fullname(doc.modified_by))
		msg = """Hello %s, <br> The Purchase Requisition %s (Category: %s, Sub category: %s) for %s has been submitted for your approval by %s.
		<br> Link: %s <br><br>Thanks,<br>Knight Frank Procurement Team
		"""%(get_user_fullname(r_email),doc.name,doc.category,doc.sub_category,doc.kf_customer,get_user_fullname(doc.modified_by),url)
		frappe.sendmail(recipients=r_email,cc=cc_email,subject=subject,content=msg)

	if 'Commercial Approver' in frappe.get_roles() and doc.workflow_state == 'Rejected by Commercial Approver':
		r_email = doc.requestor_email
		url = base_url_dev + "/material-request/" + doc.name
		comments = frappe.db.sql(''' 
			Select content from `tabComment` where reference_doctype='Material Request' 
			and reference_name=%s 
			and comment_type='comment'
			and owner = %s
			''',(doc.name,doc.modified_by),as_list=1)
		subject = """Purchase Requisition %s for %s has been Rejected by %s"""%(doc.name,doc.kf_customer,get_user_fullname(doc.modified_by))
		msg = """Hello %s, <br> The Purchase Requisition %s (Category: %s, Sub category: %s) for %s has been rejected by %s with the following Comments: %s
		<br>Link: %s <br><br>Thanks,<br>Knight Frank Procurement Team
		"""%(get_user_fullname(r_email),doc.name,doc.category,doc.sub_category,doc.kf_customer,get_user_fullname(doc.modified_by),comments[0][0],url)
		frappe.sendmail(recipients=r_email,subject=subject,content=msg)	

	if 'Procurement  Approver' in frappe.get_roles() and doc.workflow_state == 'Procurement Approver Approved':
		r_email = doc.requestor_email
		url = base_url_dev + "/material-request/" + doc.name
		subject="""Purchase Requisition %s for %s has been submitted for your Approval by %s"""%(doc.name,doc.kf_customer,get_user_fullname(doc.modified_by))
		msg = """Hello %s, <br> The Purchase Requisition %s (Category: %s, Sub category: %s) for %s has been Approved by %s
		<br>Link: %s <br><br>Thanks,<br>Knight Frank Procurement Team
		"""%(get_user_fullname(r_email),doc.name,doc.category,doc.sub_category,doc.kf_customer,get_user_fullname(doc.modified_by),url)
		frappe.sendmail(recipients=r_email,subject=subject,content=msg)	

	if 'Procurement  Approver' in frappe.get_roles() and doc.workflow_state == 'Rejected by Procurement Approver':
		r_email = doc.requestor_email
		url = base_url_dev + "/material-request/" + doc.name
		comments = frappe.db.sql(''' 
			Select content from `tabComment` where reference_doctype='Material Request' 
			and reference_name=%s 
			and comment_type='comment'
			and owner = %s
			''',(doc.name,doc.modified_by),as_list=1)
		subject = """Purchase Requisition %s for %s has been Rejected by %s"""%(doc.name,doc.kf_customer,get_user_fullname(doc.modified_by))
		msg = """Hello %s, <br> The Purchase Requisition %s (Category: %s, Sub category: %s) for %s has been rejected by %s with the following Comments : %s.
		<br>Link: %s <br><br>Thanks,<br>Knight Frank Procurement Team
		"""%(get_user_fullname(r_email),doc.name,doc.category,doc.sub_category,doc.kf_customer,get_user_fullname(doc.modified_by),comments[0][0],url)
		frappe.sendmail(recipients=r_email,subject=subject,content=msg)

def get_permission_query_conditions(doctype):
	#Commercial Approver can see only the MR for himself
	if frappe.session.user == "Administrator":
		return ""

	if "Director Approver" in frappe.get_roles() or "Procurement  Approver" in frappe.get_roles() or "Vendor" in frappe.get_roles():
		names = frappe.db.sql("""select name from `tabMaterial Request` 
								where workflow_state not in ('Created by Requestor') """)

		if names:
			names = ",".join("'" + i[0]+"'" for i in names)
			names = "(" + names + ")"

		if names:
			return """(`tabMaterial Request`.name in %s)"""%(names)

		if not names:
		#to return nothing
			return """(`tabMaterial Request`.name is NULL)"""

	if "Commercial Approver" in frappe.get_roles():
		user = frappe.session.user
		names = frappe.db.sql("""select name from `tabMaterial Request` 
								where commercial_approver=%s 
								and workflow_state not in ('Created by Requestor') """,(user))

		if names:
			names = ",".join("'" + i[0]+"'" for i in names)
			names = "(" + names + ")"

		if names:
			return """(`tabMaterial Request`.name in %s)"""%(names)

		if not names:
		#to return nothing
			return """(`tabMaterial Request`.name is NULL)"""