# Copyright (c) 2025, Dnyaneshwar pawar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ServiceBooking(Document):
	def validate(self):
		addresses = frappe.get_all(
			"Address",
			filters={
				"link_doctype": "Customer",
				"link_name": self.customer_name
			},
			fields=["name", "email_id"],
			limit_page_length=1
		)

		if addresses and addresses[0].get("email_id"):
			self.email = addresses[0]["email_id"]

		msg_doc = frappe.get_doc("Email Template", "Service Booking")
		subject = msg_doc.subject or "Your Service Booking Update"
		message = frappe.render_template(msg_doc.response_html, {"doc": self})

		if self.email:
			frappe.sendmail(
				recipients=[self.email],
				subject=subject,
				message=message,
				reference_doctype=self.doctype,
				reference_name=self.name
			)


