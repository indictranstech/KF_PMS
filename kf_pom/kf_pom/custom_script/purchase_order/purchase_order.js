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

	},
	onload:function(frm){
		if(frm.doc.workflow_state == 'Vendor Approved' && frappe.user.has_role('Vendor')) {
			//show print option 
		} else if (frm.doc.workflow_state != 'Vendor Approved' && frappe.user.has_role('Vendor')){
			//hide print option 
			$('.text-muted.btn.btn-default.icon-btn[data-original-title="Print"]').hide()
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