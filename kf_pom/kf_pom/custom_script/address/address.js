frappe.ui.form.on("Address",{ 
	onload:function(frm) {
		if(!frm.is_new()) {
			//make commercial approver madatory for customer address
			if(frm.doc.links[0].link_doctype == 'Customer') {
				cur_frm.fields_dict.commercial_approver.get_query = function (doc, cdt, cdn) {
				return { query: "kf_pom.kf_pom.custom_script.address.address.user_query" }
				}
				frm.set_df_property('commercial_approver','reqd',1)
			} else {
				frm.set_value('commercial_approver','')
				frm.set_df_property('commercial_approver','reqd',0)

			}
			//make email_id mandatory for supplier ie vendor address
			if(frm.doc.links[0].link_doctype == 'Supplier') {
				cur_frm.fields_dict.commercial_approver.get_query = function (doc, cdt, cdn) {
				return { query: "kf_pom.kf_pom.custom_script.address.address.user_query" }
				}
				frm.set_df_property('email_id','reqd',1)
			} else {
				frm.set_df_property('email_id','reqd',0)

			}
		}
	},
	sub_location:function(frm){
		cur_frm.fields_dict.commercial_approver.get_query = function (doc, cdt, cdn) {
				return { query: "kf_pom.kf_pom.custom_script.address.address.user_query" }
			}
	},
	validate:function(frm){
		//Make Commercial approver mandatory only on Customer Address
		if(frm.doc.links[0].link_doctype == 'Customer') {
			frm.set_df_property('commercial_approver','reqd',1)
		} else {
			frm.set_value('commercial_approver','')
			frm.set_df_property('commercial_approver','reqd',0)

		}
		//Make email_id mandatory for Supplier ie Vendor address
		if(frm.doc.links[0].link_doctype == 'Supplier') {
			frm.set_df_property('email_id','reqd',1)
		} else {
			frm.set_df_property('email_id','reqd',0)

		}
	}
})	