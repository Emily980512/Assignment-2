CREATE DATABASE db;
use db;

DROP TABLE IF EXISTS tasks_3034504344;

CREATE TABLE tasks_3034504344 (
    id integer PRIMARY KEY,
    title varchar(500) NOT NULL,
    is_completed INTEGER NOT NULL DEFAULT 0,
    notify varchar(500) Not NULL
    )