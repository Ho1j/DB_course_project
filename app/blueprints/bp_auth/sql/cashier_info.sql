SELECT * from cashiers
JOIN internal_users ON cashiers.user_id = internal_users.user_id
WHERE internal_users.user_id = '$user_id'
