UPDATE schedules
SET available_tickets = available_tickets + 1
WHERE schedule_id = (
    SELECT schedule_id
    FROM tickets
    WHERE ticket_id = '$ticket_id'
);
