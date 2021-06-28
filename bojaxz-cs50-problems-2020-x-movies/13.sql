/*select name from people as p
JOIN stars as s ON p.id = s.person_id
JOIN movies as m ON s.movie_id = m.id
where (name = "Kevin Bacon");*/

-- select the names of stars that have starred in a movie with Kevin Bacon.

select name from stars as s
JOIN people as p ON s.person_id = p.id
where movie_id IN (select movie_id from people JOIN stars ON s.person_id = p.id
where birth = 1958 and name = "Kevin Bacon")
and name != "Kevin Bacon";
