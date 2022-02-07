// Copyright (c) 2022, Frappe Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Storage Integration Settings', {
	refresh: function(frm) {
		
		createCustomButton(
			frm,
			"Migrate all to S3",
			"All the local files will be delete and uploaded to AWS S3 storage.",
			"storage_integration.controller.migrate_existing_files",
		);

		createCustomButton(
			frm,
			"Delete all from S3",
			"All the remote files will be deleted from S3 storage, make sure you have cloned the files for backup or restored to the local storage.",
			"storage_integration.controller.delete_all_remote",
		);

		createCustomButtonWithArgs(
			frm,
			"Clone for backup",
			"All the remote(S3) files will be downloaded to your site, this operation will not delete the remote files.",
			"storage_integration.controller.clone_files",
			"clone"
		);

		createCustomButtonWithArgs(
			frm,
			"Restore to local",
			"All the remote files will be restored locally.",
			"storage_integration.controller.clone_files",
			"restore"
		)

	}
});

function createCustomButton(frm, title, description, method) {
	return frm.add_custom_button(__(title), () => {
			frappe.confirm(description,
				() => {
					// yes
					frappe.call({
						method: method,
					})
				}
			);
		}, __("Actions"));
}

function createCustomButtonWithArgs(frm, title, description, method, action) {
	return frm.add_custom_button(__(title), () => {
			frappe.confirm(description,
				() => {
					// yes
					frappe.call({
						method: method,
						args: {
							action_type: 'restore'
						}
					})
				}
			);
		}, __("Actions"));
}
