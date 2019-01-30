CREATE TABLE user (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) NOT NULL UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    locality VARCHAR(100),
    country VARCHAR(100),
    password_hash CHAR(60) BINARY NOT NULL,
    email VARCHAR(255) NOT NULL,
    created DATETIME NOT NULL DEFAULT NOW(),
    last_updated DATETIME DEFAULT NULL ON UPDATE NOW(),
    admin_rights INT NOT NULL DEFAULT 0
);


CREATE TABLE question (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    view_count INT NOT NULL DEFAULT 0,
    vote_count INT NOT NULL DEFAULT 0,
    title VARCHAR(100) NOT NULL,
    body VARCHAR(1000),
    image_url VARCHAR(1000),
    created DATETIME NOT NULL DEFAULT NOW(),
    last_updated DATETIME DEFAULT NULL ON UPDATE NOW()
);


CREATE TABLE answer (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    question_id INT NOT NULL,
    vote_count INT NOT NULL DEFAULT 0,
    body VARCHAR(1000) NOT NULL,
    image_url VARCHAR(100),
    created DATETIME NOT NULL DEFAULT NOW(),
    last_updated DATETIME DEFAULT NULL ON UPDATE NOW()
);


CREATE TABLE comment (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    question_id INT,
    answer_id INT,
    body VARCHAR(1000),
    created DATETIME NOT NULL DEFAULT NOW(),
    last_updated DATETIME DEFAULT NULL ON UPDATE NOW()
);


CREATE TABLE tag (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE,
    user_id INT NOT NULL,
    created DATETIME NOT NULL DEFAULT NOW()
);


CREATE TABLE tag_to_question (
    question_id INT NOT NULL,
    tag_id INT NOT NULL,
    user_id INT NOT NULL,
    created DATETIME NOT NULL DEFAULT NOW()
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
ADD FOREIGN KEY (tag_id) REFERENCES tag(id) ON DELETE CASCADE
