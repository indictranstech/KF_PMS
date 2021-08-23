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
	kf_customer: function(frm){
		//to filter customer addresses in drop-down
		frm.set_query('kf_customer_shipping_address', function(doc) {
			if(!doc.kf_customer) {
				frappe.throw(_('Please select Customer'));
			}

			return {
				query: 'frappe.contacts.doctype.address.address.address_query',
				filters: {
					link_doctype: 'Customer',
					link_name: doc.kf_customer
				}
			};
		});
	},
	kf_customer_shipping_address: function(frm) {
		//to frtch customer address on PO
		if(frm.doc.kf_customer_shipping_address) {
			frappe.call({
				method: "frappe.contacts.doctype.address.address.get_address_display",
				args: {"address_dict": frm.doc.kf_customer_shipping_address },
				callback: function(r) {
					if(r.message) {
						console.log(r.message)
						frm.set_value("kf_customer_shipping_address_display", r.message)
					}
				}
			})
		} else {
			frm.set_value("kf_customer_shipping_address_display", "");
		}
		//to fetch the sub location from customer address on PO
		frappe.db.get_value('Address',frm.doc.kf_customer_shipping_address,'sub_location')
		.then(r =>{
			if(r.message){
				frm.set_value('kf_sub_location',r.message.sub_location)
			}
		})
	},
	requestor_email: function(frm) {
		//set requestor mobile no
        if(frm.doc.requestor_email){
            frappe.db.get_value('User',frm.doc.requestor_email,'mobile_no')
            .then(r => {
		        if(r.message){
		        	frm.set_value('requestor_contact_no',r.message.mobile_no)
		        }
		    })
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