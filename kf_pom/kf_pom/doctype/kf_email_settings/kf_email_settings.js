// Copyright (c) 2021, Indictranstech and contributors
// For license information, please see license.txt

frappe.ui.form.on('KF Email Settings', {
	onload: function(frm) {
		cur_frm.fields_dict.procurement_approver.get_query = function (doc, cdt, cdn) {
		return { query: "kf_pom.kf_pom.doctype.kf_email_settings.kf_email_settings.user_query_for_PA" }
		}

		cur_frm.fields_dict.director_approver.get_query = function (doc, cdt, cdn) {
		return { query: "kf_pom.kf_pom.doctype.kf_email_settings.kf_email_settings.user_query_for_DA" }
		}
	}
});
