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

	# base_url_local = "http://localhost:8002/app/"
	base_url_dev = "http://kfpom-dev.indictranstech.com/app"
	# send the emails on creation,approval and rejection
	if 'Requestor/Site Manager' in frappe.get_roles() and doc.workflow_state == 'Submitted by Requestor':
		r_email = doc.commercial_approver
		cc_email = doc.requestor_email
		url = base_url_dev + "/material-request/" + doc.name
		subject = """Purchase Requisition for %s - %s has been submitted for your Approval by %s """%(doc.kf_customer,doc.name,doc.requestor_name)
		msg = """Dear %s, <br> The Purchase Requisition %s is submitted for your approval by %s
		<br> Link : %s
		"""%(get_user_fullname(r_email),doc.name,doc.requestor_name,url)
		frappe.sendmail(recipients=r_email,cc=cc_email,subject= subject,content=msg)

	if 'Commercial Approver' in frappe.get_roles() and doc.workflow_state == 'Commercial Approver Approved':
		proc_appr = frappe.db.sql("""Select parent from `tabHas Role` where role = 'Procurement  Approver'""")
		r_email = proc_appr[0][0]
		cc_email = doc.requestor_email 
		url = base_url_dev + "/material-request/" + doc.name
		subject = """Purchase Requisition for %s - %s submitted for your Approval by %s"""%(doc.kf_customer,doc.name,get_user_fullname(doc.modified_by))
		msg = """Dear %s, <br> The Purchase Requisition %s is submitted for your approval by %s.
		<br> Link: %s
		"""%(get_user_fullname(r_email),doc.name,get_user_fullname(doc.modified_by),url)
		frappe.sendmail(recipients=r_email,cc=cc_email,subject=subject,content=msg)	

	if 'Commercial Approver' in frappe.get_roles() and doc.workflow_state == 'Rejected by Commercial Approver':
		r_email = doc.requestor_email
		url = base_url_dev + "/material-request/" + doc.name
		subject = """Purchase Requisition for %s - %s is Rejected by %s"""%(doc.kf_customer,doc.name,get_user_fullname(doc.modified_by))
		msg = """Dear %s, <br> The Purchase Requisition %s is rejected by %s with the following Comments: %s
		<br>Link: %s
		"""%(get_user_fullname(r_email),doc.name,get_user_fullname(doc.modified_by),comments[0][0],url)
		frappe.sendmail(recipients=r_email,subject=subject,content=msg)	

	if 'Procurement  Approver' in frappe.get_roles() and doc.workflow_state == 'Procurement Approver Approved':
		r_email = doc.requestor_email
		url = base_url_dev + "/material-request/" + doc.name
		subject="""Purchase Requisition for %s - %s is submitted for your Approval by %s"""%(doc.kf_customer,doc.name,get_user_fullname(doc.modified_by))
		msg = """Dear %s, <br> The Purchase Requisition %s is Approved by %s
		<br>Link: %s
		"""%(get_user_fullname(r_email),doc.name,get_user_fullname(doc.modified_by),url)
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
		subject = """Purchase Requisition for %s - %s is Rejected by %s"""%(doc.kf_customer,doc.name,get_user_fullname(doc.modified_by))
		msg = """Dear %s, <br> The Purchase Requisition %s is Rejected by %s with the following Comments : %s.
		<br>Link: %s
		"""%(get_user_fullname(r_email),doc.name,get_user_fullname(doc.modified_by),comments[0][0],url)
		frappe.sendmail(recipients=r_email,subject=subject,content=msg)	

def get_permission_query_conditions(doctype):
	#Commercial Approver can see only the MR for himself
	if frappe.session.user == "Administrator" or "Director Approver" in frappe.get_roles() or "Procurement  Approver" in frappe.get_roles() or "Vendor" in frappe.get_roles():
		return ""

	if "Commercial Approver" in frappe.get_roles():
		user = frappe.session.user
		names = frappe.db.sql("""select name from `tabMaterial Request` 
								where commercial_approver=%s """,(user))

		if names:
			names = ",".join("'" + i[0]+"'" for i in names)
			names = "(" + names + ")"

		if names:
			return """(`tabMaterial Request`.name in %s)"""%(names)

		if not names:
		#to return nothing
			return """(`tabMaterial Request`.name is NULL)"""