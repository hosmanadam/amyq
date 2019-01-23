CREATE TABLE questions (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    view_count INT NOT NULL DEFAULT 0,
    vote_count INT NOT NULL DEFAULT 0,
    title VARCHAR(100) NOT NULL,
    body VARCHAR(1000),
    image_url VARCHAR(1000),
    time_submitted DATETIME NOT NULL DEFAULT NOW()
);


CREATE TABLE answers (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    question_id INT NOT NULL,
    vote_count INT NOT NULL DEFAULT 0,
    body VARCHAR(1000) NOT NULL,
    image_url VARCHAR(100),
    time_submitted DATETIME NOT NULL DEFAULT NOW()
);


CREATE TABLE comments (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    question_id INT,
    answer_id INT,
    body VARCHAR(1000),
    time_submitted DATETIME NOT NULL DEFAULT NOW()
);


CREATE TABLE tags (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL
);


CREATE TABLE tags_to_questions (
    question_id INT NOT NULL,
    tag_id INT NOT NULL
);


ALTER TABLE answers
ADD FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE;


ALTER TABLE comments
ADD FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE;


ALTER TABLE comments
ADD FOREIGN KEY (answer_id) REFERENCES answers(id) ON DELETE CASCADE;


ALTER TABLE tags_to_questions
ADD FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE;


ALTER TABLE tags_to_questions
ADD FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
