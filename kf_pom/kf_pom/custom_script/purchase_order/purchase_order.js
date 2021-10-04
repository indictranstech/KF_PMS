frappe.ui.form.on("Purchase Order",{
	setup: function(frm) {
		console.log('In setup')
		frappe.flag_for_category = 0
	},
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
		// 	//hide comment box
		// 	$('.comment-box').hide();
			frm.set_df_property("approver_comments","hidden",1)
		}
		if(frm.is_new()){
			frm.set_value("tc_name",'Standard Template')
			frm.set_value("kf_contact_name","Sarvesh Tiwari")
            frm.set_value("kf_contact_email","sarvesh.tiwari@in.knightfrank.com")
            frm.set_value("kf_contact_no","8291900219")

		}
	},
	onload:function(frm){
		frappe.flag_for_category = 1
    	// frm.set_value('kf_purchase_requisition',frm.doc.items[0].material_request)

		if(frm.is_new()){
			frm.set_value("tc_name",'Standard Template')
			frm.set_value("kf_contact_name","Sarvesh Tiwari")
            frm.set_value("kf_contact_email","sarvesh.tiwari@in.knightfrank.com")
            frm.set_value("kf_contact_no","8291900219")

			if(frm.doc.company_billing_add){
				frm.set_value('billing_address',frm.doc.company_billing_add)
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
		// 	//hide comment box
		// 	$('.comment-box').hide();
			frm.set_df_property("approver_comments","hidden",1)
		}
	},
	category: function(frm) {
		if (frappe.flag_for_category == 1) {
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
    	} else {
    		if(frm.doc.category){
	        	// frm.set_value('sub_category','')
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
    },
	kf_contact_email: function(frm) {
        if(frm.doc.kf_contact_email) {
            frappe.call({
                method: 'frappe.client.get_value',
                args: {
                    'doctype': 'User',
                    'filters': {'name': frm.doc.kf_contact_email},
                    'fieldname': [
                        'mobile_no',
                        'full_name'
                    ]
                },
                callback: function(r) {
                    if (!r.exc) {
                        // code snippet
                        if(r.message){
                            frm.set_value("kf_contact_name",r.message.full_name)
                            frm.set_value("kf_contact_no",r.message.mobile_no)
                        }
                    }
                }
            });
        } else {
            frm.set_value("kf_contact_name","")
            frm.set_value("kf_contact_no","")
        }
    },
	company_billing_add:function(frm) {
		if(frm.doc.company_billing_add) {
			frm.set_value('billing_address',frm.doc.company_billing_add)
			frm.set_value('shipping_address',frm.doc.company_billing_add)
		}
	},
	supplier: function(frm){
		if(frm.doc.company_billing_add) {
			frm.set_value('billing_address',frm.doc.company_billing_add)
			frm.set_value('shipping_address',frm.doc.company_billing_add)
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
    	frm.set_value('kf_purchase_requisition',frm.doc.items[0].material_request)
    }
});