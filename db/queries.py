read_questions = """
    SELECT * FROM questions
"""

read_question = """
    SELECT * FROM questions
    WHERE id = %(id)s
"""

read_answer = """
    SELECT * FROM answers
    WHERE id = %(id)s
"""

read_answers = """
    SELECT * FROM answers
    WHERE question_id = %(id)s
    ORDER BY time_submitted DESC
"""

read_comment = """
    SELECT * FROM comments
    WHERE id = %(id)s
"""

add_question = """
    INSERT INTO questions
        (title, body, image_url)
    VALUES
        (%(title)s, %(body)s, %(image_url)s)
"""

update_question = """
    UPDATE questions
    SET title=%(title)s, body=%(body)s, image_url=%(image_url)s
    WHERE id=%(id)s
"""

update_answer = """
    UPDATE answers
    SET body=%(body)s, image_url=%(image_url)s
    WHERE id=%(id)s
"""

update_comment = """
    UPDATE comments
    SET body=%(body)s
    WHERE id=%(id)s
"""

add_answer = """
    INSERT INTO answers
        (question_id, body, image_url)
    VALUES
        (%(question_id)s, %(body)s, %(image_url)s)
"""

read_latest_content_match_id = """
    SELECT id FROM questions
    WHERE title = %(title)s
    ORDER BY time_submitted DESC
    LIMIT 1
"""

read_question_id_for_answer_id = """
    SELECT question_id FROM answers
    WHERE id = %(id)s
"""

update_question_vote_count = """
    UPDATE questions
    SET vote_count = vote_count + %(value)s
    WHERE id = %(id)s
"""

update_answer_vote_count = """
    UPDATE answers
    SET vote_count = vote_count + %(value)s
    WHERE id = %(id)s
"""

delete_question = """
    DELETE FROM questions
    WHERE id = %(id)s
"""

delete_answer = """
    DELETE FROM answers
    WHERE id = %(id)s
"""

delete_comment = """
    DELETE FROM comments
    WHERE id = %(id)s
"""

add_question_comment = """
    INSERT INTO comments
        (question_id, body)
    VALUES
        (%(question_id)s, %(body)s)
"""

add_answer_comment = """
    INSERT INTO comments
        (answer_id, body)
    VALUES
        (%(answer_id)s, %(body)s)
"""

read_comments_for_question = """
    SELECT * FROM comments
    WHERE question_id = %(question_id)s
    ORDER BY time_submitted
"""

read_comments_for_answer = """
    SELECT * FROM comments
    WHERE answer_id = %(answer_id)s
    ORDER BY time_submitted
"""

read_questions_for_search = """
    SELECT
        questions.id, questions.title, questions.view_count, questions.vote_count, questions.time_submitted
    FROM
        questions LEFT JOIN answers ON questions.id = answers.question_id
    WHERE
        questions.title LIKE CONCAT('%', %(search)s, '%') OR
        questions.body LIKE CONCAT('%', %(search)s, '%') OR
        answers.body LIKE CONCAT('%', %(search)s, '%')
    GROUP BY questions.id
"""