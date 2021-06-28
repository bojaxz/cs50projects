-- select movies released in 2010 and their ratings sorted by rating and then title
select title, rating from movies as m JOIN ratings as r on r.movie_id = m.id where year = 2010 order by rating desc, title;