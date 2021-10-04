frappe.ui.form.on("Item",{
	refresh:function(frm){
		cur_frm.fields_dict['sub_category'].get_query = function(doc, cdt, cdn) {
		    return {
		        filters: [
		            		['Sub Category','category', '=', frm.doc.category]
						]
			}
		}	
	},
	category: function(frm) {
        if(frm.doc.category){
            frm.set_value('sub_category','')
            cur_frm.fields_dict['sub_category'].get_query = function(doc, cdt, cdn) {
                return {
                    filters: [
                                ['Sub Category','category', '=', frm.doc.category]
                            ]
                }
            } 
        } else {
            frm.set_value('sub_category','')
        }
    }
});