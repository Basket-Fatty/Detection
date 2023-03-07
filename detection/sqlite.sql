CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name varchar(20) NOT NULL,
  password varchar(20) NOT NULL
  ) 
INSERT INTO user(name,password) VALUES ('zyl','123456'),('admin','123456');