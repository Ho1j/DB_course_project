UPDATE schedules
SET available_tickets = available_tickets - 1
WHERE schedule_id = '$schedule_id' AND available_tickets > 0;
