frappe.pages['storage-backups'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Storage Integration Backups',
		single_column: true
	});
}