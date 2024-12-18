drop table goal_reached;
drop table game;
drop table goal;
create table high_score(
id int not null auto_increment,
player_name varchar(40) default null,
time int default null,
money int default null,
distance int default null,
flight_count int default null,
country_count int default null,
continent_count int default null,
route varchar(40)default null,
points int default null,
primary key(id)
);
delete from airport
where type = "heliport";

delete from airport
where type = "balloonport";

delete from airport
where type = "seaplane_base";

delete from airport
where type = "closed";