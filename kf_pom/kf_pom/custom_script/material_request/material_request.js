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
        if(frappe.user.has_role('Requestor/Site Manager')) {
            frm.set_df_property('approver_comments','read_only',1)
        }
        if((frm.doc.workflow_state=="Rejected by Procurement Approver"||frm.doc.workflow_state=="Submitted by Requestor") && frappe.user.has_role('Commercial Approver')) {
            frm.set_df_property('approver_comments','reqd',1)
        }
        if(frm.is_new()){
            frm.set_value("tc_name",'Standard Template')
            frm.set_value("kf_contact_name","Sarvesh Tiwari")
            frm.set_value("kf_contact_email","Sarvesh.Tiwari@in.knightfrank.com")
            frm.set_value("kf_contact_no","9999911111")

        }
	},
	onload:function(frm) {
        if(frm.is_new()) {
            frm.set_value('requestor_email',frappe.session.user_email);
            frm.set_value('requestor_name',frappe.session.user_fullname);
        }
        if(frm.is_new()){
            frm.set_value("tc_name",'Standard Template')
            frm.set_value("kf_contact_name","Sarvesh Tiwari")
            frm.set_value("kf_contact_email","Sarvesh.Tiwari@in.knightfrank.com")
            frm.set_value("kf_contact_no","9999911111")

        }
    },
    kf_customer: function(frm){
        //to filter customer addresses in drop-down
        frm.set_value("kf_customer_shipping_address","")
        
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