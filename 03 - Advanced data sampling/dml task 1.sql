--Задание 1

insert into artist (name)
values
('Eminem'),
('50 Cent'),
('Linkin Park'),
('OneRepublic'),
('Джиган'),
('Ольга Бузова');

insert into genre (title)
values ('rap'), ('rock'), ('pop'), ('Hip-hop');

insert into album (title, release_year)
values 
('Kamikaze', 2018),
('Best of 50 Cent', 2019),
('Lost Demos', 2020),
('Better Days', 2019),
('Край рая', 2019),
('Альбом 1', 2018);

insert into track (title, duration, album_id)
values 
('Superman', '5:50', 1),
('In Da Club', '4:20', 2),
('my name is', '4:06', 1),
('Papercut', '3:20', 3),
('Apologize', '4:10', 4),
('ДНК', '3:24', 5),
('Мандаринка', '2:33', 6);

insert into collection (title, release_year)
values 
('Сборник 1', 2018),
('Сборник 2', 2019),
('Сборник 3', 2019),
('Сборник 4', 2020);

insert into genre_artist (genre_id, artist_id)
values 
(1, 1),
(1, 2),
(1, 5),
(2, 3),
(2, 4),
(3, 6),
(4, 1),
(4, 5);

insert into album_artist (album_id, artist_id)
values 
(1, 1),
(1, 2),
(1, 3),
(2, 2),
(2, 1),
(3, 1),
(3, 3),
(4, 4),
(5, 5),
(5, 6),
(6, 6),
(6, 5);

insert into track_collection (track_id, collection_id)
values 
(2, 1),
(2, 2),
(3, 2),
(4, 1),
(4, 2),
(4, 3),
(4, 4),
(5, 1),
(6, 1),
(6, 2),
(7, 4);








