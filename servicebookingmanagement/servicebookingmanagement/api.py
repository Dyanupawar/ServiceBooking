import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def get_service_bookings(service_type=None, status=None):
    filters = {}
    if service_type:
        filters["service_type"] = service_type
    if status:
        filters["status"] = status

    bookings = frappe.get_all(
        "Service Booking",
        fields=["name", "customer_name", "service_type", "preferred_datetime", "status"],
        filters=filters,
        order_by="preferred_datetime desc"
    )

    results = []

    for booking in bookings:
        try:
            customer = frappe.get_doc("Customer", booking.customer_name)
        except frappe.DoesNotExistError:
            customer = None

        results.append({
            "booking_id": booking.name,
            "service_type": booking.service_type,
            "status": booking.status,
            "preferred_datetime": booking.preferred_datetime,
            "customer": {
                "name": customer.customer_name if customer else booking.customer_name,
                "territory": customer.territory if customer else "",
                "customer_group": customer.customer_group if customer else ""
            }
        })

    return {
        "success": True,
        "count": len(results),
        "data": results
    }
