-- select name from people as p JOIN stars as s ON p.id = s.person_id where movie_id IN (select title from movies where title like "Toy Story%")
-- select * from movies where id IN (select movie_id from stars where person_id = (select id from people where name ="Ryan Reynolds"));
-- select the names of stars in the toy story movies
select name from people where id IN (select person_id from stars where movie_id = (select id from movies where title ="Toy Story"));