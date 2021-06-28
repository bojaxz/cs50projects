-- select movies that Helena star in
select title from movies as m
JOIN stars as s ON m.id = s.movie_id
JOIN people as p ON s.person_id = p.id
where name = "Helena Bonham Carter"
-- compare the results with movies Johnny stars in and merge the similarities
Intersect
select title from movies as m
JOIN stars as s ON m.id = s.movie_id
JOIN people as p ON s.person_id = p.id
where name = "Johnny Depp";

