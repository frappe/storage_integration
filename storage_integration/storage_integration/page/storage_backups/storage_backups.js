frappe.pages['storage-backups'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Storage Integration Backups',
		single_column: true
	});

	page.add_inner_button(__("Create Backup"), function () {
		frappe.call({
			method: "storage_integration.storage_integration.page.storage_backups.storage_backups.create_backups",
			callback: (r) => {
				frappe.msgprint("Backup scheduled for now. You can download it from this page once it is complete.")
			},
		});
	});

	$(frappe.render_template("storage_backups")).appendTo(page.body.addClass("no-border"));
}
