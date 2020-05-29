drop database if exists restaurant;

create database if not exists restaurant default character set utf8 collate utf8_general_ci;
use restaurant;

create table if not exists business
(
  business_id  varchar(55)   not null,
  name         varchar(255)  not null,
  address      varchar(255)  not null,
  city         varchar(45)   not null,
  state        varchar(5)    not null,
  postal_code  int           not null,
  latitude     double        not null,
  longitude    double        not null,
  stars        decimal(2, 1) not null,
  review_count int           not null,
  is_open      boolean       not null,
  primary key (business_id)
) ENGINE = InnoDB;

create table if not exists attributes
(
  business_id                varchar(55) not null,
  RestaurantsTakeOut         boolean     not null,
  RestaurantsDelivery        boolean     not null,
  RestaurantsReservations    boolean     not null,
  BusinessAcceptsCreditCards boolean     not null,
  RestaurantsPriceRange2     boolean     not null,
  RestaurantsGoodForGroups   boolean     not null,
  GoodForKids                boolean     not null,
  HasTV                      boolean     not null,
  OutdoorSeating             boolean     not null,
  WiFi                       boolean     not null,
  RestaurantsTableService    boolean     not null,
  Caters                     boolean     not null,
  BikeParking                boolean     not null,
  primary key (business_id),
  foreign key (business_id) references business (business_id)
    on update cascade
    on delete cascade,
  index using btree (business_id)
) ENGINE = InnoDB;

create table if not exists user
(
  user_id        varchar(55)   not null,
  name           varchar(55)   not null,
  review_count   int           not null,
  yelping_since  datetime      not null,
  fans           int           not null,
  average_stars  decimal(3, 2) not null,
  email          varchar(50)   not null,
  password       varchar(20)   not null,
  positive_votes int           not null,
  negative_votes int           not null,
  primary key (user_id)
) ENGINE = InnoDB;

create table if not exists review
(
  review_id      varchar(55) not null,
  user_id        varchar(55) not null,
  business_id    varchar(55) not null,
  stars          tinyint     not null,
  text           text        not null,
  review_date    datetime    not null,
  positive_votes int         not null,
  negative_votes int         not null,
  primary key (review_id),
  foreign key (user_id) references user (user_id)
    on update cascade
    on delete cascade,
  foreign key (business_id) references business (business_id)
    on update cascade
    on delete cascade,
  index using btree (user_id),
  index using btree (business_id)
) ENGINE = InnoDB;

create table if not exists categories
(
  business_id varchar(55) not null,
  categories  varchar(30) not null,
  primary key (business_id, categories),
  foreign key (business_id) references business (business_id)
    on update cascade
    on delete cascade,
  index using btree (business_id)
) ENGINE = InnoDB;

create table if not exists admin
(
  admin_id varchar(55) not null,
  email    varchar(50) not null,
  password varchar(50) not null,
  primary key (admin_id)
) ENGINE = InnoDB;

create table if not exists collections
(
  user_id     varchar(55) not null,
  business_id varchar(55) not null,
  primary key (user_id, business_id),
  foreign key (user_id) references user (user_id)
    on update cascade
    on delete cascade,
  foreign key (business_id) references business (business_id)
    on update cascade
    on delete cascade,
  index using btree (user_id)
) ENGINE = InnoDB;

create table if not exists checkin
(
  id          int         not null auto_increment,
  business_id varchar(55) not null,
  date        datetime    not null,
  primary key (id),
  foreign key (business_id) references business (business_id)
    on update cascade
    on delete cascade,
  index using btree (business_id)
) ENGINE = InnoDB;

create table if not exists fact
(
  yelping_since  datetime      not null,
  user_id        varchar(55)   not null,
  business_id    varchar(55)   not null,
  review_count   int           not null,
  average_stars  decimal(3, 2) not null,
  positive_votes int           not null,
  negative_votes int           not null,
  primary key (yelping_since, user_id, business_id),
  foreign key (user_id) references user (user_id)
    on update cascade
    on delete cascade,
  foreign key (business_id) references business (business_id)
    on update cascade
    on delete cascade,
  index using btree (yelping_since),
  index using btree (user_id),
  index using btree (business_id)
) ENGINE = InnoDB;

insert into fact
select user.yelping_since, temp.*
from user,
     (select user_id,
             business_id,
             count(*)            as review_count,
             avg(stars)          as average_stars,
             sum(positive_votes) as positive_votes,
             sum(negative_votes) as negative_votes
      from review
      group by user_id, business_id) as temp
where user.user_id = temp.user_id;