frappe.ui.form.on("Purchase Order",{
	refresh:function(frm){
		cur_frm.fields_dict['sub_category'].get_query = function(doc, cdt, cdn) {
		    return {
		        filters: [
		            		['Sub Category','category', '=', frm.doc.category]
						]
			}
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