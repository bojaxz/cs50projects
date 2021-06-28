-- return the names of the top 5 highest rated films that Chadwick Boseman has starred in
select title from movies as m JOIN stars as s ON m.id = s.movie_id JOIN people as p ON s.person_id = p.id JOIN ratings as r ON m.id = r.movie_id where name ="Chadwick Boseman"
order by rating limit 5;