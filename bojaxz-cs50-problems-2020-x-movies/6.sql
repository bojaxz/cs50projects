-- compute the average ratings of movies released in 2012
select avg(rating) from ratings where movie_id IN (select id from movies where year = 2012);