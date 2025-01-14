def create_orders_list(result):
    orders = {}
    for order in result:
        order_id = order['order_id']
        if order_id not in orders:
            orders[order_id] = {
                'booking_date': order['booking_date'],
                'email': order['email'],
                'tickets': []
            }
        if order['ticket_id']:
            orders[order_id]['tickets'].append({
                'ticket_id': order['ticket_id'],
                'flight_number': order['flight_number'],
                'schedule_date': order['schedule_date'],
                'departure_time': order['departure_time'],
                'arrival_time': order['arrival_time'],
                'passport': order['passport'],
                'first_name': order['first_name'],
                'last_name': order['last_name'],
                'birth_date': order['birth_date'],
                'seat_number': order['seat_number'],
                'price': order['price'],
                'status': order['status']
            })
    return orders