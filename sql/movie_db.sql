DROP DATABASE IF EXISTS movie_db;
CREATE DATABASE IF NOT EXISTS movie_db;
USE movie_db;

-- 电影表（movies）
CREATE TABLE movies (
    movie_id BIGINT NOT NULL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    release_date VARCHAR(100),
    total_box_office DECIMAL(15,2),
    avg_ticket_price DECIMAL(6,2),
    screening_count INT,
    attendance_rate DECIMAL(5,2),
    country VARCHAR(50),
    overall_rating DECIMAL(3,1),
    description TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 导演表（directors）
CREATE TABLE directors (
    director_id BIGINT NOT NULL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    gender TINYINT COMMENT '0:未知 1:男 2:女',
    birth_date DATE,
    nationality VARCHAR(50)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 演员表（actors）
CREATE TABLE actors (
    actor_id BIGINT NOT NULL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    gender TINYINT COMMENT '0:未知 1:男 2:女',
    birth_date DATE,
    nationality VARCHAR(50)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 类型表（categories）
CREATE TABLE categories (
    genre_id BIGINT NOT NULL PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    description VARCHAR(200)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 电影-导演关联表（movie_directors）
CREATE TABLE movie_directors (
    id BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    movie_id BIGINT NOT NULL,
    director_id BIGINT NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
    FOREIGN KEY (director_id) REFERENCES directors(director_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 电影-演员关联表（movie_actors）
CREATE TABLE movie_actors (
    id BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    movie_id BIGINT NOT NULL,
    actor_id BIGINT NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
    FOREIGN KEY (actor_id) REFERENCES actors(actor_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 电影-类型关联表（movie_categories）
CREATE TABLE movie_categories (
    id BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    movie_id BIGINT NOT NULL,
    genre_id BIGINT NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
    FOREIGN KEY (genre_id) REFERENCES categories(genre_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 电影-时间关联表
CREATE TABLE daily_box_office (
    date_time VARCHAR(100),
    movie_id BIGINT NOT NULL,
    box_office DECIMAL(15,2),
    attendees BIGINT,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
    PRIMARY KEY (movie_id, date_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 用户表（users）
CREATE TABLE users (
    user_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    real_name VARCHAR(50),
    phone VARCHAR(20),
    role_type TINYINT NOT NULL COMMENT '1:管理员 2:普通用户',
    email VARCHAR(100),
    create_time DATETIME NOT NULL,
    update_time DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 为关联表创建复合索引（提高查询性能）
CREATE INDEX idx_movie_director ON movie_directors(movie_id, director_id);
CREATE INDEX idx_movie_actor ON movie_actors(movie_id, actor_id);
CREATE INDEX idx_movie_genre ON movie_categories(movie_id, genre_id);
