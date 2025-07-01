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
    id BIGINT NOT NULL PRIMARY KEY,
    movie_id BIGINT NOT NULL,
    director_id BIGINT NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
    FOREIGN KEY (director_id) REFERENCES directors(director_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 电影-演员关联表（movie_actors）
CREATE TABLE movie_actors (
    id BIGINT NOT NULL PRIMARY KEY,
    movie_id BIGINT NOT NULL,
    actor_id BIGINT NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
    FOREIGN KEY (actor_id) REFERENCES actors(actor_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 电影-类型关联表（movie_categories）
CREATE TABLE movie_categories (
    id BIGINT NOT NULL PRIMARY KEY,
    movie_id BIGINT NOT NULL,
    genre_id BIGINT NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
    FOREIGN KEY (genre_id) REFERENCES categories(genre_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 用户表（users）
CREATE TABLE users (
    user_id BIGINT NOT NULL PRIMARY KEY,
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

INSERT INTO movies (movie_id, title, release_date, total_box_office, avg_ticket_price, screening_count, attendance_rate, country, overall_rating, description) VALUES
(1, '肖申克的救赎', '1994-09-23', 28340000.00, 8.50, 12000, 85.50, '美国', 9.3, '一位银行家被冤枉入狱，在监狱中展现非凡毅力和智慧的故事'),
(2, '阿甘正传', '1994-07-06', 677400000.00, 9.20, 18000, 90.20, '美国', 9.2, '一个智商不高但心地善良的男子见证美国历史重大事件的故事'),
(3, '泰坦尼克号', '1997-12-19', 2187000000.00, 10.50, 25000, 95.80, '美国', 9.1, '豪华邮轮上的跨阶级爱情悲剧'),
(4, '盗梦空间', '2010-07-16', 836800000.00, 12.00, 15000, 88.30, '美国', 9.0, '关于梦境入侵的科幻惊悚片'),
(5, '霸王别姬', '1993-01-01', 30000000.00, 5.50, 8000, 75.20, '中国', 9.6, '两位京剧艺人跨越半个世纪的悲欢离合'),
(6, '这个杀手不太冷', '1994-09-14', 46000000.00, 7.80, 10000, 82.40, '法国', 9.4, '职业杀手与小女孩的感人故事'),
(7, '星际穿越', '2014-11-07', 677500000.00, 11.50, 14000, 87.60, '美国', 9.3, '宇航员穿越虫洞寻找新家园的科幻冒险'),
(8, '千与千寻', '2001-07-20', 355000000.00, 8.20, 12000, 92.10, '日本', 9.3, '小女孩在神灵世界的奇幻冒险'),
(9, '教父', '1972-03-24', 245100000.00, 6.50, 10000, 89.70, '美国', 9.2, '黑手党家族的兴衰史诗'),
(10, '疯狂动物城', '2016-03-04', 1023000000.00, 10.80, 20000, 94.50, '美国', 9.0, '兔子警官和狐狸骗子联手破案的动画喜剧');

INSERT INTO directors (director_id, name, gender, birth_date, nationality) VALUES
(1, '弗兰克·德拉邦特', 1, '1959-01-28', '美国'),
(2, '罗伯特·泽米吉斯', 1, '1952-05-14', '美国'),
(3, '詹姆斯·卡梅隆', 1, '1954-08-16', '加拿大'),
(4, '克里斯托弗·诺兰', 1, '1970-07-30', '英国'),
(5, '陈凯歌', 1, '1952-08-12', '中国'),
(6, '吕克·贝松', 1, '1959-03-18', '法国'),
(7, '宫崎骏', 1, '1941-01-05', '日本'),
(8, '弗朗西斯·福特·科波拉', 1, '1939-04-07', '美国'),
(9, '拜伦·霍华德', 1, '1968-12-26', '美国'),
(10, '李安', 1, '1954-10-23', '中国台湾');

INSERT INTO actors (actor_id, name, gender, birth_date, nationality) VALUES
(1, '蒂姆·罗宾斯', 1, '1958-10-16', '美国'),
(2, '摩根·弗里曼', 1, '1937-06-01', '美国'),
(3, '汤姆·汉克斯', 1, '1956-07-09', '美国'),
(4, '莱昂纳多·迪卡普里奥', 1, '1974-11-11', '美国'),
(5, '凯特·温斯莱特', 2, '1975-10-05', '英国'),
(6, '约瑟夫·高登-莱维特', 1, '1981-02-17', '美国'),
(7, '张国荣', 1, '1956-09-12', '中国香港'),
(8, '张丰毅', 1, '1956-09-01', '中国'),
(9, '让·雷诺', 1, '1948-07-30', '法国'),
(10, '娜塔莉·波特曼', 2, '1981-06-09', '美国'),
(11, '马修·麦康纳', 1, '1969-11-04', '美国'),
(12, '安妮·海瑟薇', 2, '1982-11-12', '美国'),
(13, '柊瑠美', 2, '1987-08-01', '日本'),
(14, '马龙·白兰度', 1, '1924-04-03', '美国'),
(15, '阿尔·帕西诺', 1, '1940-04-25', '美国'),
(16, '金妮弗·古德温', 2, '1978-05-22', '美国'),
(17, '杰森·贝特曼', 1, '1969-01-14', '美国');

INSERT INTO categories (genre_id, name, description) VALUES
(1, '剧情', '以人物情感和关系发展为核心的电影类型'),
(2, '爱情', '主要讲述爱情故事的电影'),
(3, '科幻', '基于科学假设和想象的虚构故事'),
(4, '动画', '通过动画技术制作的电影'),
(5, '犯罪', '涉及犯罪行为和司法系统的电影'),
(6, '奇幻', '包含魔法或其他超自然元素的电影'),
(7, '惊悚', '制造紧张和悬念的电影'),
(8, '历史', '基于历史事件或人物的电影'),
(9, '喜剧', '以幽默和搞笑为主要特点的电影'),
(10, '动作', '包含大量动作场面的电影');

INSERT INTO movie_directors (id, movie_id, director_id) VALUES
(1, 1, 1),
(2, 2, 2),
(3, 3, 3),
(4, 4, 4),
(5, 5, 5),
(6, 6, 6),
(7, 7, 4),
(8, 8, 7),
(9, 9, 8),
(10, 10, 9);

INSERT INTO movie_actors (id, movie_id, actor_id) VALUES
(1, 1, 1),
(2, 1, 2),
(3, 2, 3),
(4, 3, 4),
(5, 3, 5),
(6, 4, 4),
(7, 4, 6),
(8, 5, 7),
(9, 5, 8),
(10, 6, 9),
(11, 6, 10),
(12, 7, 11),
(13, 7, 12),
(14, 8, 13),
(15, 9, 14),
(16, 9, 15),
(17, 10, 16),
(18, 10, 17);

INSERT INTO movie_categories (id, movie_id, genre_id) VALUES
(1, 1, 1),
(2, 1, 5),
(3, 2, 1),
(4, 2, 8),
(5, 3, 1),
(6, 3, 2),
(7, 4, 3),
(8, 4, 7),
(9, 5, 1),
(10, 5, 8),
(11, 6, 5),
(12, 6, 10),
(13, 7, 3),
(14, 7, 1),
(15, 8, 4),
(16, 8, 6),
(17, 9, 1),
(18, 9, 5),
(19, 10, 4),
(20, 10, 9);

INSERT INTO users (user_id, username, password, real_name, phone, role_type, email, create_time, update_time) VALUES
(1, 'admin', 'admin123', '系统管理员', '13800138000', 1, 'admin@example.com', '2023-01-01 10:00:00', '2023-01-01 10:00:00'),
(2, 'john_doe', 'john123', '约翰·多伊', '13912345678', 2, 'john.doe@example.com', '2023-02-15 14:30:00', '2023-02-15 14:30:00'),
(3, 'jane_smith', 'jane456', '简·史密斯', '13987654321', 2, 'jane.smith@example.com', '2023-03-10 09:15:00', '2023-03-10 09:15:00'),
(4, 'michael_wang', 'mike789', '王麦克', '13811223344', 2, 'michael.wang@example.com', '2023-04-05 16:45:00', '2023-04-05 16:45:00'),
(5, 'sarah_li', 'sarah101', '李莎拉', '13755667788', 2, 'sarah.li@example.com', '2023-05-20 11:20:00', '2023-05-20 11:20:00'),
(6, 'david_zhang', 'david202', '张大卫', '13699887766', 2, 'david.zhang@example.com', '2023-06-12 13:10:00', '2023-06-12 13:10:00'),
(7, 'emily_chen', 'emily303', '陈艾米丽', '13544556677', 2, 'emily.chen@example.com', '2023-07-08 08:30:00', '2023-07-08 08:30:00'),
(8, 'robert_liu', 'robert404', '刘罗伯特', '13477889900', 2, 'robert.liu@example.com', '2023-08-25 15:50:00', '2023-08-25 15:50:00'),
(9, 'lisa_zhao', 'lisa505', '赵丽莎', '13311223344', 2, 'lisa.zhao@example.com', '2023-09-18 10:40:00', '2023-09-18 10:40:00'),
(10, 'kevin_sun', 'kevin606', '孙凯文', '13255667788', 2, 'kevin.sun@example.com', '2023-10-30 17:25:00', '2023-10-30 17:25:00');