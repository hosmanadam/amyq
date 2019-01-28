read_questions = """
    SELECT * FROM questions
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

read_question = """
    SELECT * FROM questions
    WHERE id = %(id)s
"""

read_answers = """
    SELECT * FROM answers
    WHERE question_id = %(id)s
    ORDER BY time_submitted DESC
"""

read_answer = """
    SELECT * FROM answers
    WHERE id = %(id)s
"""

read_comment = """
    SELECT * FROM comments
    WHERE id = %(id)s
"""

read_existing_tags = """
    SELECT * FROM tags
"""

read_tags_for_question = """
    SELECT tags.name, tags.id
    FROM tags JOIN tags_to_questions ON tags.id = tags_to_questions.tag_id
    WHERE question_id = %(question_id)s
    ORDER BY tags.name
"""

read_tag_id_for_tag_name = """
    SELECT id FROM tags
    WHERE name=%(name)s
"""

read_comments_for_question = """
    SELECT * FROM comments
    WHERE question_id = %(question_id)s
    ORDER BY time_submitted DESC
"""

read_comments_for_answer = """
    SELECT * FROM comments
    WHERE answer_id = %(answer_id)s
    ORDER BY time_submitted DESC
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

add_question = """
    INSERT INTO questions
        (title, body, image_url)
    VALUES
        (%(title)s, %(body)s, %(image_url)s)
"""

add_new_tag = """
    INSERT INTO tags
        (name)
    VALUES
        (%(name)s)
"""

add_existing_tag_to_question = """
    INSERT INTO tags_to_questions
        (question_id, tag_id)
    VALUES
        (%(question_id)s, %(tag_id)s)
"""

add_answer = """
    INSERT INTO answers
        (question_id, body, image_url)
    VALUES
        (%(question_id)s, %(body)s, %(image_url)s)
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

increment_question_view_count = """
    UPDATE questions
    SET view_count = view_count + 1
    WHERE id = %(id)s
"""

delete_question = """
    DELETE FROM questions
    WHERE id = %(id)s
"""

delete_tag_from_question = """
    DELETE FROM tags_to_questions
    WHERE question_id = %(question_id)s AND tag_id = %(tag_id)s
"""

delete_answer = """
    DELETE FROM answers
    WHERE id = %(id)s
"""

delete_comment = """
    DELETE FROM comments
    WHERE id = %(id)s
"""
