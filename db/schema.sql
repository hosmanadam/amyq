CREATE TABLE user (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) NOT NULL,
    admin_rights INT NOT NULL DEFAULT 0,
    password_hash CHAR(60) BINARY NOT NULL,
    email VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    locality VARCHAR(100),
    country VARCHAR(100),
    facebook_username VARCHAR(50),
    github_username VARCHAR(39),
    twitter_username VARCHAR(15),
    linkedin_profile_url VARCHAR(100),
    created DATETIME NOT NULL DEFAULT NOW(),
    last_updated DATETIME DEFAULT NULL ON UPDATE NOW(),
    UNIQUE KEY (username),
    UNIQUE KEY (email)
);


CREATE TABLE question (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    body VARCHAR(30000),
    image_url VARCHAR(2083),
    created DATETIME NOT NULL DEFAULT NOW(),
    last_updated DATETIME DEFAULT NULL ON UPDATE NOW()
);


CREATE TABLE answer (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    question_id INT NOT NULL,
    body VARCHAR(30000) NOT NULL,
    image_url VARCHAR(2083),
    created DATETIME NOT NULL DEFAULT NOW(),
    last_updated DATETIME DEFAULT NULL ON UPDATE NOW(),
    accepted DATETIME DEFAULT NULL
);


CREATE TABLE comment (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    question_id INT DEFAULT NULL,
    answer_id INT DEFAULT NULL,
    body VARCHAR(30000),
    created DATETIME NOT NULL DEFAULT NOW(),
    last_updated DATETIME DEFAULT NULL ON UPDATE NOW()
);


CREATE TABLE tag (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    user_id INT NOT NULL,
    created DATETIME NOT NULL DEFAULT NOW(),
    UNIQUE KEY (name)
);


CREATE TABLE tag_to_question (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    question_id INT NOT NULL,
    tag_id INT NOT NULL,
    user_id INT NOT NULL,
    created DATETIME NOT NULL DEFAULT NOW(),
    UNIQUE KEY (user_id, question_id)
);


CREATE TABLE view (                                        -- One entry per user per question
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    question_id INT DEFAULT NULL,
    count INT NOT NULL,
    created DATETIME NOT NULL DEFAULT NOW(),
    last_updated DATETIME DEFAULT NULL ON UPDATE NOW(),
    UNIQUE KEY (user_id, question_id)
);


CREATE TABLE vote (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    value INT NOT NULL,                                    -- 1=up, -1=down
    question_id INT DEFAULT NULL,
    answer_id INT DEFAULT NULL,
    created DATETIME NOT NULL DEFAULT NOW(),
    last_updated DATETIME DEFAULT NULL ON UPDATE NOW(),
    UNIQUE KEY (user_id, question_id, answer_id)
);



ALTER TABLE question
ADD FOREIGN KEY (user_id) REFERENCES user(id);


ALTER TABLE answer
ADD FOREIGN KEY (user_id) REFERENCES user(id);

ALTER TABLE answer
ADD FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE;


ALTER TABLE comment
ADD FOREIGN KEY (user_id) REFERENCES user(id);

ALTER TABLE comment
ADD FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE;

ALTER TABLE comment
ADD FOREIGN KEY (answer_id) REFERENCES answer(id) ON DELETE CASCADE;


ALTER TABLE tag
ADD FOREIGN KEY (user_id) REFERENCES user(id);


ALTER TABLE tag_to_question
ADD FOREIGN KEY (user_id) REFERENCES user(id);

ALTER TABLE tag_to_question
ADD FOREIGN KEY (question_id) REFERENCES question (id) ON DELETE CASCADE;

ALTER TABLE tag_to_question
ADD FOREIGN KEY (tag_id) REFERENCES tag(id) ON DELETE CASCADE;


ALTER TABLE view
ADD FOREIGN KEY (user_id) REFERENCES user(id);

ALTER TABLE view
ADD FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE;


ALTER TABLE vote
ADD FOREIGN KEY (user_id) REFERENCES user(id);

ALTER TABLE vote
ADD FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE;

ALTER TABLE vote
ADD FOREIGN KEY (answer_id) REFERENCES answer(id) ON DELETE CASCADE;
