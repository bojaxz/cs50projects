-- select name from people where id IN (select person_id from stars where movie_id = (select id from movies where year =2004))
-- select the names of stars in movies released in 2004 sorted by their birthdays
select name from people as p JOIN stars as s ON p.id = s.person_id JOIN movies as m ON s.movie_id = m.id where year = 2004 order by birth;