frappe.ui.form.on("Material Request",{
	refresh:function(frm){
        $.each(frm.doc.items, function(i,v) {
              frappe.model.set_value(v.doctype, v.name, "schedule_date", frm.doc.schedule_date);                           
              frappe.item_quantity += v.qty
        });
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
            frm.set_value("kf_contact_email","sarvesh.tiwari@in.knightfrank.com")
            frm.set_value("kf_contact_no","8291900219")
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
	onload:function(frm) {
        var item_quantity = 0
        $.each(frm.doc.items, function(i,v) {                       
              item_quantity += v.qty
        });
        frappe.call({
            method: 'kf_pom.kf_pom.custom_script.material_request.material_request.check_po',
            args: {
                'mi': frm.doc.name
            },
            callback: function(r) {
                if(r.message)
                {
                    if(r.message[0].tot_qty == item_quantity)
                    {
                        frm.remove_custom_button(__("Create"))
                    }
                }
            }
        });
        if(frm.is_new()) {
            frm.set_value('requestor_email',frappe.session.user_email);
            frm.set_value('requestor_name',frappe.session.user_fullname);
            frm.set_value('schedule_date',frappe.datetime.add_days(frappe.datetime.get_today(), 3))
        }
        if(frm.is_new()){
            frm.set_value("tc_name",'Standard Template')
            frm.set_value("kf_contact_name","Sarvesh Tiwari")
            frm.set_value("kf_contact_email","sarvesh.tiwari@in.knightfrank.com")
            frm.set_value("kf_contact_no","8291900219")
        }
        frm.set_query('kf_customer_shipping_address', function(doc) {
            if(!doc.kf_customer) {
                frappe.throw(_('Please select Customer'));
            }

            return {
                // query: 'frappe.contacts.doctype.address.address.address_query',
                query: 'kf_pom.kf_pom.custom_script.material_request.material_request.address_query',
                filters: {
                    link_doctype: 'Customer',
                    link_name: doc.kf_customer
                }
            };
        });
    },
    company: function(frm) {
        frm.set_query('billing_address', function(doc) {

            return {
                // query: 'frappe.contacts.doctype.address.address.address_query',
                query: 'kf_pom.kf_pom.custom_script.material_request.material_request.address_query',
                filters: {
                    link_doctype: 'Company',
                    link_name: doc.company
                }
            };
        });
    },
    billing_address:function(frm) {
        if(frm.doc.billing_address) {
            frm.set_value('company_billing_add',frm.doc.billing_address)
        } else {
            frm.set_value('company_billing_add','')
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
                // query: 'frappe.contacts.doctype.address.address.address_query',
                query: 'kf_pom.kf_pom.custom_script.material_request.material_request.address_query',
                filters: {
                    link_doctype: 'Customer',
                    link_name: doc.kf_customer
                }
            };
        });
    },
    kf_customer_shipping_address: function(frm) {
        //to fetch customer address on PO
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
        }

        if(frm.doc.kf_customer_shipping_address) {
            frappe.call({
                method: "kf_pom.kf_pom.custom_script.material_request.material_request.get_address_details",
                args: {"name": frm.doc.kf_customer_shipping_address },
                callback: function(r) {
                    if(r.message) {
                        frm.set_value('kf_sub_location',r.message[0].sub_location)
                        frm.set_value('commercial_approver',r.message[0].commercial_approver)
                    }
                }
            })
        } else {
            frm.set_value("kf_customer_shipping_address_display", "");
            frm.set_value('kf_sub_location',"")
            frm.set_value('commercial_approver',"")
        }
        
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