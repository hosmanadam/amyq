INSERT INTO questions
    (id, view_count, vote_count, title, body, image_url, time_submitted)
VALUES
    (1, 3, 3, 'Whats the meaning of life?', 'Ive wondered about this since I was a kid, please let me know ASAP', NULL, '2011-10-09 12:11:11'),
    (2, 4, 4, 'Why is the sky blue?', 'I wont be able to sleep until you answer, please help!!!', NULL, '2012-10-09 13:11:11');


INSERT INTO answers
    (id, question_id, vote_count, body, image_url, time_submitted)
VALUES
    (1, 1, 3, '42,  you dummy', NULL, '2010-10-10 11:11:11'),
    (2, 1, 4, '42 like the other guy says', NULL, '2011-10-10 12:11:11'),
    (3, 2, 5, 'cause its not red', NULL, '2012-10-10 13:11:11');


INSERT INTO comments
    (id, question_id, answer_id, body, time_submitted)
VALUES
    (1, 1, 1, 'please dont be so rude', '2010-10-10 11:11:11');


INSERT INTO tags
    (id, name)
VALUES
    (1, 'meaningoflife'),
    (2, 'naturessecrets'),
    (3, 'colorsareawesome');


INSERT INTO tags_to_questions
    (question_id, tag_id)
VALUES
    (1, 1),
    (2, 2),
    (2, 3);
