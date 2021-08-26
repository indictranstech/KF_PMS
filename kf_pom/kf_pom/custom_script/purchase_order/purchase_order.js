frappe.ui.form.on("Purchase Order",{
	refresh:function(frm){
		cur_frm.fields_dict['sub_category'].get_query = function(doc, cdt, cdn) {
		    return {
		        filters: [
		            		['Sub Category','category', '=', frm.doc.category]
						]
			}
		}
		if(frm.doc.workflow_state == 'Vendor Approved' && frappe.user.has_role('Vendor')) {
			//show print option 
		} else if (frm.doc.workflow_state != 'Vendor Approved' && frappe.user.has_role('Vendor')){
			//hide print option 
			$('.text-muted.btn.btn-default.icon-btn[data-original-title="Print"]').hide()
		}
		if(frappe.user.has_role('Vendor')){
			//hide comments
			$('.timeline-items').hide();
			//hide comment box
			$('.comment-box').hide();
			frm.set_df_property("approver_comments","hidden",1)
		}
		if(frm.is_new()){
			frm.set_value("tc_name",'Standard Template')
			frm.set_value("kf_contact_name","Sarvesh Tiwari")
			frm.set_value("kf_contact_email","Sarvesh.Tiwari@in.knightfrank.com")
			frm.set_value("kf_contact_no","9999911111")

		}
	},
	onload:function(frm){
		if(frm.is_new()){
			frm.set_value("tc_name",'Standard Template')
			frm.set_value("kf_contact_name","Sarvesh Tiwari")
			frm.set_value("kf_contact_email","Sarvesh.Tiwari@in.knightfrank.com")
			frm.set_value("kf_contact_no","9999911111")

		}
		if(frm.doc.workflow_state == 'Vendor Approved' && frappe.user.has_role('Vendor')) {
			//show print option 
		} else if (frm.doc.workflow_state != 'Vendor Approved' && frappe.user.has_role('Vendor')){
			//hide print option 
			$('.text-muted.btn.btn-default.icon-btn[data-original-title="Print"]').hide()
		}
		if(frappe.user.has_role('Vendor')){
			//hide comments
			$('.timeline-items').hide();
			//hide comment box
			$('.comment-box').hide();
			frm.set_df_property("approver_comments","hidden",1)
		}
	},
	validate:function(frm){
        var from_date=new Date(frm.doc.po_validity_from_date);
        var to_date=new Date(frm.doc.po_validity_to_date);
    	if (from_date && to_date){
    		if (from_date>to_date){
    			frappe.throw("From Date Should not Exceed To Date")
    		}
    	}
    }
});