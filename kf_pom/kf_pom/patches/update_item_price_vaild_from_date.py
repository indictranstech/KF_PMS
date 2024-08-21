import frappe

def execute():
    frappe.log_error(title = 'Patch execute', message='Patch execute')
    frappe.db.sql("update `tabItem Price` set valid_from= '2030-01-01'")