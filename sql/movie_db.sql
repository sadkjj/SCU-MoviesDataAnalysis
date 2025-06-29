-- Create the database
CREATE DATABASE IF NOT EXISTS movie_db;
USE movie_db;

-- Create the movies table
CREATE TABLE IF NOT EXISTS movies (
    movie_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_date DATE NOT NULL,
    rating DECIMAL(4,3),
    box_office_usd BIGINT,
    release_region VARCHAR(255),
    genres VARCHAR(255),
    directors VARCHAR(255)
);

-- Insert the movie data
INSERT INTO movies (title, release_date, rating, box_office_usd, release_region, genres, directors) VALUES
('死神来了6：血脉诅咒', '2025-05-14', 7.206, 280004566, 'United States of America', '恐怖, 悬疑', '亚当 B·斯坦因, 扎克·利波夫斯基'),
('星际宝贝史迪奇', '2025-05-17', 7.100, 910349181, 'United States of America', '家庭, 科幻, 喜剧, 冒险', '迪恩·弗莱舍·坎普'),
('新·驯龙高手', '2025-06-06', 7.909, 358189000, 'United States of America', '奇幻, 家庭, 动作', '迪恩·德布洛斯'),
('惊变28年', '2025-06-18', 7.125, 62805230, 'United Kingdom, United States of America', '恐怖, 惊悚, 科幻', '丹尼·博伊尔'),
('谍网追凶', '2025-04-09', 6.972, 95956038, 'United States of America', '惊悚, 动作', '詹姆斯·霍斯'),
('我的世界大电影', '2025-03-31', 6.500, 951514812, 'Sweden, United States of America', '家庭, 喜剧, 冒险, 奇幻', '杰瑞德·赫斯'),
('会计刺客2', '2025-04-23', 7.216, 102123366, 'United States of America', '悬疑, 犯罪, 惊悚', '加文·欧康诺'),
('罪人', '2025-04-16', 7.557, 362889145, 'United States of America', '恐怖, 奇幻, 惊悚', '瑞恩·库格勒'),
('碟中谍8：最终清算', '2025-05-17', 7.200, 540612404, 'United States of America', '动作, 冒险, 惊悚', '克里斯托弗·麦夸里'),
('犯罪都市4', '2024-04-24', 6.856, 83703350, 'South Korea', '动作, 犯罪, 剧情, 惊悚, 喜剧', '许明行'),
('疾速追杀：芭蕾杀姬', '2025-06-04', 7.100, 100818000, 'United States of America', '动作, 惊悚, 犯罪', '伦·怀斯曼'),
('制暴：无限杀机', '2025-03-26', 6.698, 99068160, 'United Kingdom, United States of America', '动作, 犯罪, 惊悚', '大卫·阿耶'),
('白雪公主', '2025-03-12', 4.300, 205067778, 'United States of America', '家庭, 奇幻', '马克·韦伯'),
('丑陋的继姐', '2025-03-07', 7.159, 884602, 'Denmark, Norway, Poland, Sweden', '恐怖, 喜剧, 奇幻, 剧情', 'Emilie Blichfeldt'),
('地球特派员', '2025-06-18', 6.733, 35000000, 'United States of America', '家庭, 喜剧, 冒险, 动画, 科幻', '石之予, 玛德琳·莎拉芬, 阿德里安·莫利纳'),
('雷霆特攻队*', '2025-04-30', 7.402, 380591509, 'United States of America', '动作, 科幻, 冒险', '杰克·施莱尔'),
('海洋奇缘2', '2024-11-21', 7.078, 1059242164, 'Canada, United States of America', '动画, 冒险, 家庭, 喜剧', '小戴夫·德里克, 杰森·汉德, 达娜·莱杜克斯·米勒'),
('战·争', '2025-04-09', 7.177, 31896828, 'United Kingdom, United States of America', '战争, 动作', 'Ray Mendoza, 亚历克斯·加兰'),
('腓尼基计划', '2025-05-23', 6.925, 27449265, 'United States of America, Germany', '冒险, 喜剧', '韦斯·安德森'),
('幽冥部队', '2025-05-01', 6.402, 4307562, 'United States of America', '动作, 剧情, 惊悚', '乔·卡纳汉'),
('美国队长4', '2025-02-12', 6.076, 415101577, 'United States of America', '动作, 惊悚, 科幻', '朱利叶斯·约拿'),
('直到黎明', '2025-04-23', 6.602, 52794193, 'United States of America', '恐怖, 悬疑', '大卫·F·桑德伯格'),
('刺猬索尼克3', '2024-12-19', 7.708, 492162604, 'United States of America, Japan', '动作, 科幻, 喜剧, 家庭', '杰夫·福勒'),
('功夫梦：融合之道', '2025-05-08', 6.900, 98176000, 'United States of America', '动作, 冒险, 剧情', '乔纳森·恩特威斯尔'),
('驯龙高手3', '2019-01-03', 7.750, 524580592, 'United States of America', '动画, 家庭, 冒险', '迪恩·德布洛斯'),
('在失落之地', '2025-02-27', 6.529, 4755330, 'Germany, Switzerland', '动作, 奇幻, 冒险', '保罗·安德森');

-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    account_id VARCHAR(10) UNIQUE NOT NULL,
    name VARCHAR(50) NOT NULL,
    gender ENUM('男', '女', '其他') NOT NULL,
    password VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) AUTO_INCREMENT = 20250001;  -- 设置账号ID从20250001开始

-- 插入5个用户数据
INSERT INTO users (account_id, name, gender, password) VALUES
('20250001', '张三', '男', 'zhang123!'),
('20250002', '李四', '男', 'li456@'),
('20250003', '王五', '男', 'wang789#'),
('20250004', '赵六', '女', 'zhao101$'),
('20250005', '钱七', '女', 'qian202%');