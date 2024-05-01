from orders.models import Order
from customer.models import Return
from django.db.models import Sum


def calculate_retention_rate(start_date, end_date, obj):

    # Count the number of unique customers who made purchases within the date range
    retained_customers = Order.objects.filter(
        status__in=[
            Order.ORDER_PLACED, Order.ORDER_PROCESSING, Order.PACKED,
            Order.READY_FOR_DISPATCH, Order.SHIPPED, Order.DELIVERED
        ],
        purchase__purchase_date__range=(start_date, end_date)
    ).distinct().count()

    # Total number of unique customers at the start of the period
    total_customers_at_start = obj.count()

    # Calculate retention rate (as percentage)
    if total_customers_at_start > 0:
        retention_rate = (retained_customers / total_customers_at_start) * 100
    else:
        retention_rate = 0.0

    return retention_rate


def calculate_clv(customer):
    total_orders = Order.objects.filter(user=customer.username)
    total_revenue = total_orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    total_orders_count = total_orders.count()

    if total_orders_count > 0:
        clv = total_revenue / total_orders_count
    else:
        clv = 0

    return clv


def order_processing_time():
    # Filter orders that are both placed and shipped
    processed_orders = Order.objects.filter(status=Order.ORDER_PLACED, shipping_id__isnull=False)

    # Calculate processing time for each order
    processing_times = []
    for order in processed_orders:
        placement_time = order.created_at  # Assuming 'created_at' is the timestamp when order was placed
        shipment_time = order.shipped_at  # Assuming 'shipped_at' is the timestamp when order was shipped

        if placement_time and shipment_time:
            processing_time = shipment_time - placement_time
            processing_times.append(processing_time.total_seconds() / 3600)  # Convert to hours

    # Calculate average processing time
    if processing_times:
        average_processing_time = sum(processing_times) / len(processing_times)
    else:
        average_processing_time = 0  # Default value if no processed orders found

    return average_processing_time


def order_return_rate():
    # Count total number of orders
    total_orders = Order.objects.count()

    # Count number of orders with associated completed returns
    returned_orders = Order.objects.filter(return__isnull=False, return__status=Return.APPROVED).distinct().count()

    # Calculate order return rate (as percentage)
    if total_orders > 0:
        return_rate_percentage = (returned_orders / total_orders) * 100
    else:
        return_rate_percentage = 0  # Default value if no orders exist

    return return_rate_percentage



