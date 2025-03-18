create table if not exists workers (
    id serial primary key,
    worker_name varchar (100) not null unique,
    department varchar (100) not null,
    boss_id integer references workers(id) on delete set null 
); 