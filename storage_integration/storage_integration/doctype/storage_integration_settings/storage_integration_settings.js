// Copyright (c) 2022, Frappe Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Storage Integration Settings', {
	refresh: function(frm) {

		frm.add_custom_button(__("Migrate All"), () => {
			frappe.confirm('All the local file attachments will be uploaded to AWS S3. Are you sure you want to proceed?',
				() => {
					// yes
					frappe.call({
						method: 'storage_integration.controller.migrate_existing_files',
					})
				}, () => {
					// no
				}
			);
		});

		frm.add_custom_button(__("Remove All"), () => {
			frappe.confirm('All the remote(S3) attachments will be deleted, make sure you have taken the backups. Are you sure you want to proceed?',
				() => {
					// yes
					frappe.call({
						method: 'storage_integration.controller.remove_all_data',
					})
				}, () => {
					// no
				}
			);
		});

	}
});
