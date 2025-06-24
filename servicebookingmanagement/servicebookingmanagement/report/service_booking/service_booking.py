# Copyright (c) 2025, Dnyaneshwar pawar and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data




def get_data(filters):
    conditions = []
    values = []

    if filters.get("service_type"):
        conditions.append("service_type = %s")
        values.append(filters["service_type"])

    if filters.get("status"):
        conditions.append("status = %s")
        values.append(filters["status"])

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

    query = f'''
        SELECT 
            customer_name,
            service_type,
            status,
            preferred_datetime AS time
        FROM `tabService Booking`
        {where_clause}
    '''

    return frappe.db.sql(query, values=values, as_dict=1)





def get_columns():
	return [
		{
			
			"fieldname": "customer_name",
			"label":"Customer Name",
			"fieldtype": "Link",
			"options":"Customer",	
			"width":120
		},
		{
			
			"fieldname": "service_type",
			"label":"Service Type",
			"fieldtype": "Data",
			"width":120
		},
		{
			
			"fieldname": "time",
			"label":"Preferred Date/Time",
			"fieldtype": "Data",
			"width":120
		},
		{
			
			"fieldname": "status",
			"label":"Status",
			"fieldtype": "Data",
			"width":120
		}
	]