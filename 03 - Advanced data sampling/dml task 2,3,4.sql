-- Задание 2

-- Название и продолжительность самого длительного трека.
select title, duration
from track 
where duration = (select MAX(duration) from track);

--Название треков, продолжительность которых не менее 3,5 минут.
select title, duration
from track 
where duration >= '3:30';

--Названия сборников, вышедших в период с 2018 по 2020 год включительно.
select title, release_year
from collection
where release_year between 2018 and 2020;

--Исполнители, чьё имя состоит из одного слова.
select name
from artist
where name not like '% %';

--Название треков, которые содержат слово «мой» или «my».
select title
from track
where title like '%мой%' or title like '%my%';


--Задание 3

--Количество исполнителей в каждом жанре.
select genre_id, COUNT(*) as artist_count 
from genre_artist 
group by genre_id 
order by artist_count DESC; 

-- Количество треков, вошедших в альбомы 2019–2020 годов.
select count (distinct t.id)
from track t 
join album a on t.album_id = a.id 
where a.release_year between 2019 and 2020; 

--Средняя продолжительность треков по каждому альбому.
select a.title as title_album, AVG(t.duration) as dur
from album a 
join track t on a.id = t.album_id 
group by a.title

--Все исполнители, которые не выпустили альбомы в 2020 году.
select distinct name
from artist 
where id not in (
    select distinct artist_id
    from album_artist
    where album_id in (
        select id
        from album
        where release_year = 2020
    )
);

--Названия сборников, в которых присутствует конкретный исполнитель (выберите его сами).
select distinct c.title
from collection c 
join track_collection tc on c.id = tc.collection_id 
join track t on tc.track_id = t.id 
join album a on t.album_id = a.id 
join album_artist aa on a.id = aa.album_id 
join artist a2 on aa.artist_id = a2.id 
where a2.name = 'Джиган'


-- Задание 4

--Названия альбомов, в которых присутствуют исполнители более чем одного жанра.
select distinct a.title
from album a 
join album_artist aa on a.id = aa.album_id 
join artist a2 on aa.artist_id = a2.id 
join genre_artist ga on a2.id = ga.artist_id 
group by a.id, a.title
having count(distinct ga.genre_id) > 1; 

--Наименования треков, которые не входят в сборники.
select title
from collection c 
left join track_collection tc on tc.track_id = c.id 
where tc.track_id is null;

--Исполнитель или исполнители, написавшие самый короткий по продолжительности трек, — теоретически таких треков может быть несколько.
select distinct name
from artist 
left join album_artist aa on artist.id = aa.artist_id 
left join album a on aa.album_id = a.id 
left join track t on a.id = t.album_id 
where duration = (select min(duration) from track);

--Названия альбомов, содержащих наименьшее количество треков.
select distinct a.title
from album a 
left join track t on t.album_id = a.id 
group by a.id, a.title
having count(t.id)=(
    select min(track_count) 
    from (
        select count(*) as track_count
        from track
        group by album_id 
    ) as subquery
);




















