create table if not exists genre (
    id serial primary key,
    title VARCHAR(255) not null unique 
);

create table if not exists artist (
    id serial primary key,
    name VARCHAR(255) not null unique,
    alias VARCHAR(255) unique
);

create table if not exists genre_artist (
    genre_id integer references genre(id),
    artist_id integer references artist(id),
    constraint genre_artist_pk primary key (genre_id, artist_id)
);

create table if not exists album ( 
    id serial primary key,
    title VARCHAR(255) not null,
    release_year integer not null
);

create table if not exists album_artist (
    album_id integer references album(id),
    artist_id integer references artist(id),
    constraint album_artist_pk primary key (album_id, artist_id)
);

create table if not exists track ( 
    id serial primary key,
    title VARCHAR(255) not null,
    duration integer not null,
    album_id integer references album(id)
);

create table if not exists collection ( 
    id serial primary key,
    title VARCHAR(255) not null,
    release_year integer not null
);

create table if not exists track_collection (
    track_id integer references track(id),
    collection_id integer references collection(id),
    constraint track_collection_pk primary key (track_id, collection_id)
);


