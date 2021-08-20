frappe.ui.form.on("Material Request",{
	refresh:function(frm){
		if(frm.is_new()) {
            frm.set_value('requestor_email',frappe.session.user_email);
            frm.set_value('requestor_name',frappe.session.user_fullname);
        } 
        else {
            $('.timeline-items').refresh()
        }
		
		cur_frm.fields_dict['sub_category'].get_query = function(doc, cdt, cdn) {
		    return {
		        filters: [
		            		['Sub Category','category', '=', frm.doc.category]
						]
			}
		}
        if(frappe.user.has_role('Requestor/Site Manager')) {
            frm.set_df_property('approver_comments','read_only',1)
        }
        if((frm.doc.workflow_state=="Rejected by Procurement Approver"||frm.doc.workflow_state=="Submitted by Requestor") && frappe.user.has_role('Commercial Approver')) {
            frm.set_df_property('approver_comments','reqd',1)
        }
	},
	onload:function(frm) {
        if(frm.is_new()) {
            frm.set_value('requestor_email',frappe.session.user_email);
            frm.set_value('requestor_name',frappe.session.user_fullname);
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