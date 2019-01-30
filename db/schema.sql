CREATE TABLE users (
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


CREATE TABLE questions (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    view_count INT NOT NULL DEFAULT 0,
    vote_count INT NOT NULL DEFAULT 0,
    title VARCHAR(100) NOT NULL,
    body VARCHAR(1000),
    image_url VARCHAR(1000),
    time_submitted DATETIME NOT NULL DEFAULT NOW()
);


CREATE TABLE answers (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    question_id INT NOT NULL,
    vote_count INT NOT NULL DEFAULT 0,
    body VARCHAR(1000) NOT NULL,
    image_url VARCHAR(100),
    time_submitted DATETIME NOT NULL DEFAULT NOW()
);


CREATE TABLE comments (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    question_id INT,
    answer_id INT,
    body VARCHAR(1000),
    time_submitted DATETIME NOT NULL DEFAULT NOW()
);


CREATE TABLE tags (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE,
    user_id INT NOT NULL
);


CREATE TABLE tags_to_questions (
    question_id INT NOT NULL,
    tag_id INT NOT NULL,
    user_id INT NOT NULL
);



ALTER TABLE questions
ADD FOREIGN KEY (user_id) REFERENCES users(id);


ALTER TABLE answers
ADD FOREIGN KEY (user_id) REFERENCES users(id);

ALTER TABLE answers
ADD FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE;


ALTER TABLE comments
ADD FOREIGN KEY (user_id) REFERENCES users(id);

ALTER TABLE comments
ADD FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE;

ALTER TABLE comments
ADD FOREIGN KEY (answer_id) REFERENCES answers(id) ON DELETE CASCADE;


ALTER TABLE tags
ADD FOREIGN KEY (user_id) REFERENCES users(id);


ALTER TABLE tags_to_questions
ADD FOREIGN KEY (user_id) REFERENCES users(id);

ALTER TABLE tags_to_questions
ADD FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE;


ALTER TABLE tags_to_questions
ADD FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
