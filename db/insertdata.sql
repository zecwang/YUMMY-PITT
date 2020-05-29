use restaurant;

load data infile 'D:/workspace/python/Web Demo/Dataset/data/business.csv'
  into table business
  fields terminated by ','
  optionally enclosed by '"'
  lines terminated by '\n'
  ignore 1 lines;

load data infile 'D:/workspace/python/Web Demo/Dataset/data/attributes.csv'
  into table attributes
  fields terminated by ','
  optionally enclosed by '"'
  lines terminated by '\n'
  ignore 1 lines;

load data infile 'D:/workspace/python/Web Demo/Dataset/data/user.csv'
  into table user
  fields terminated by ','
  optionally enclosed by '"'
  lines terminated by '\n'
  ignore 1 lines;

# load data infile 'D:/workspace/python/Web Demo/Dataset/data/review.csv'
#   into table review
#   fields terminated by ','
#   optionally enclosed by '"'
#   escaped by '"'
#   lines terminated by '\n'
#   ignore 1 lines;

load data infile 'D:/workspace/python/Web Demo/Dataset/data/categories.csv'
  into table categories
  fields terminated by ','
  optionally enclosed by '"'
  lines terminated by '\n'
  ignore 1 lines
  (business_id, categories)
  set id = null;

# load data infile 'D:/workspace/python/Web Demo/Dataset/data/collections.csv'
#   into table collections
#   fields terminated by ','
#   enclosed by '"'
#   escaped by '"'
#   lines terminated by '\n'
#   ignore 1 lines
#   (user_id, business_id)
#   set id = null;

load data infile 'D:/workspace/python/Web Demo/Dataset/data/checkin.csv'
  into table checkin
  fields terminated by ','
  optionally enclosed by '"'
  lines terminated by '\n'
  ignore 1 lines
  (business_id, date)
  set id = null;