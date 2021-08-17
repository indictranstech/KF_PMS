frappe.ui.form.on("Material Request",{
	refresh:function(frm){
		if(frm.is_new()) {
            frm.set_value('requestor_email',frappe.session.user_email);
            frm.set_value('requestor_name',frappe.session.user_fullname);
        }
		
		cur_frm.fields_dict['sub_category'].get_query = function(doc, cdt, cdn) {
		    return {
		        filters: [
		            		['Sub Category','category', '=', frm.doc.category]
						]
			}
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