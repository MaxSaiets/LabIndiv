## Схема БД (PostgreSQL)

### Таблиця `users`
- `id` (PK, int)
- `email` (varchar(255), unique, not null)
- `password_hash` (varchar(255), not null)
- `display_name` (varchar(120), null)
- `created_at` (datetime, not null)

### Таблиця `hashtag_requests`
- `id` (PK, int)
- `user_id` (FK → `users.id`, not null)
- `post_text` (text, not null)
- `hashtags` (text, not null) — збережено як рядок: `#tag1 #tag2 #tag3`
- `created_at` (datetime, not null)

### Зв’язки
- `users (1) -> (N) hashtag_requests`

### Як перевірити, що дані реально в PostgreSQL (для скріншота)
У Render → PostgreSQL → “Connect” / “PSQL” можна виконати:

```sql
select * from users order by id desc;
select * from hashtag_requests order by id desc limit 20;
```


