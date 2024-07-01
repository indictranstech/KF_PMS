from __future__ import unicode_literals
from frappe.model.document import Document
import frappe
import json
from frappe.utils.user import get_user_fullname
from frappe.desk.search import sanitize_searchfield
from frappe.model.db_query import DatabaseQuery


def validate(doc,method=None):
	# update amount for all the entries in items table and calculate the grand_total
	if(len(doc.items)>0):
		grand_total = 0.00
		for item in doc.items:
			amount = float(item.rate)*item.qty
			item.amount = amount
			grand_total= grand_total + amount
		doc.grand_total = grand_total

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
		s_email = frappe.db.get_singles_dict("KF Email Settings")
		r_email = doc.commercial_approver
		cc_email = doc.requestor_email
		url = base_url_dev + "/material-request/" + doc.name
		subject = """Purchase Requisition %s for %s has been submitted for your Approval by %s """%(doc.name,doc.kf_customer,doc.requestor_name)
		msg = """Hello %s, <br> The Purchase Requisition %s (Category: %s, Sub category: %s) for %s has been submitted for your approval by %s
		<br> Link : %s <br><br>Thanks,<br>Knight Frank Procurement Team
		"""%(get_user_fullname(r_email),doc.name,doc.category,doc.sub_category,doc.kf_customer,doc.requestor_name,url)
		if s_email["email_configuration"] == "1":
			frappe.sendmail(recipients=r_email,cc=cc_email,subject= subject,content=msg)

	if 'Commercial Approver' in frappe.get_roles() and doc.workflow_state == 'Commercial Approver Approved':
		cc_email = doc.requestor_email 
		s_email = frappe.db.get_singles_dict("KF Email Settings")
		r_email = s_email["procurement_approver"]
		url = base_url_dev + "/material-request/" + doc.name
		subject = """Purchase Requisition %s for %s has been submitted for your Approval by %s"""%(doc.name,doc.kf_customer,get_user_fullname(doc.modified_by))
		msg = """Hello %s, <br> The Purchase Requisition %s (Category: %s, Sub category: %s) for %s has been submitted for your approval by %s.
		<br> Link: %s <br><br>Thanks,<br>Knight Frank Procurement Team
		"""%(get_user_fullname(r_email),doc.name,doc.category,doc.sub_category,doc.kf_customer,get_user_fullname(doc.modified_by),url)
		if s_email["email_configuration"] == "1":
			frappe.sendmail(recipients=r_email,cc=cc_email,subject=subject,content=msg)

	if 'Commercial Approver' in frappe.get_roles() and doc.workflow_state == 'Rejected by Commercial Approver':
		s_email = frappe.db.get_singles_dict("KF Email Settings")
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
		if s_email["email_configuration"] == "1":
			frappe.sendmail(recipients=r_email,subject=subject,content=msg)	

	if 'Procurement  Approver' in frappe.get_roles() and doc.workflow_state == 'Procurement Approver Approved':
		s_email = frappe.db.get_singles_dict("KF Email Settings")
		r_email = doc.requestor_email
		url = base_url_dev + "/material-request/" + doc.name
		subject="""Purchase Requisition %s for %s has been submitted for your Approval by %s"""%(doc.name,doc.kf_customer,get_user_fullname(doc.modified_by))
		msg = """Hello %s, <br> The Purchase Requisition %s (Category: %s, Sub category: %s) for %s has been Approved by %s
		<br>Link: %s <br><br>Thanks,<br>Knight Frank Procurement Team
		"""%(get_user_fullname(r_email),doc.name,doc.category,doc.sub_category,doc.kf_customer,get_user_fullname(doc.modified_by),url)
		if s_email["email_configuration"] == "1":
			frappe.sendmail(recipients=r_email,subject=subject,content=msg)	

	if 'Procurement  Approver' in frappe.get_roles() and doc.workflow_state == 'Rejected by Procurement Approver':
		s_email = frappe.db.get_singles_dict("KF Email Settings")
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
		if s_email["email_configuration"] == "1":
			frappe.sendmail(recipients=r_email,subject=subject,content=msg)

# def get_permission_query_conditions(doctype):
def get_permission_query_conditions(user=None, doctype=None):
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


 # To include the addres_line1 in address drop-down on PR
@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def address_query(doctype, txt, searchfield, start, page_len, filters):
	from frappe.desk.reportview import get_match_cond

	link_doctype = filters.pop('link_doctype')
	link_name = filters.pop('link_name')
	add_name = get_match_cond(doctype)
	_add = add_name.split(" in ")
	name = tuple(_add[1][1:-2].replace("'", "").split(","))
	name_of_add = """and REPLACE(`tabAddress`.name,"'", "") in """+str(name)

	return frappe.db.sql("""select `tabAddress`.name, `tabAddress`.address_line1,`tabAddress`.city
					from 
						`tabAddress`,`tabDynamic Link` 
					where
						`tabDynamic Link`.parent = `tabAddress`.name and
						`tabDynamic Link`.parenttype = 'Address' and
						`tabDynamic Link`.link_doctype = %(link_doctype)s and 
						REPLACE(`tabDynamic Link`.link_name, "'", "") = %(link_name)s and
						ifnull(`tabAddress`.disabled, 0) = 0
						{mcond}
						order by
						if(locate(%(_txt)s, `tabAddress`.address_line1), locate(%(_txt)s, `tabAddress`.address_line1), 99999),
						`tabAddress`.idx desc, `tabAddress`.address_line1
						limit %(start)s, %(page_len)s""".format(
							mcond=name_of_add,
							key=searchfield
							), {
							'txt': '%' + txt + '%',
							'_txt': txt.replace("%", ""),
							'start': start,
							'page_len': page_len,
							'link_name': link_name.replace("'", ""),
							'link_doctype': link_doctype
						})




@frappe.whitelist()
def check_po(mi):
	return frappe.db.sql("""
		select 
			ifnull(SUM(po.total_qty),0) as tot_qty
		from 
			`tabPurchase Order` po, `tabPurchase Order Item` poi
		where
			po.name = poi.parent and po.docstatus = 0 and 
			poi.material_request = '{0}'""".format(mi),as_dict=1,debug=0)
	

@frappe.whitelist()
def get_address_details(name):
	return frappe.db.get_values("Address", name, ['sub_location','commercial_approver'], as_dict=1)


