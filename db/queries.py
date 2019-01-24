read_questions = """
    SELECT * FROM questions
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

add_question = """
    INSERT INTO questions
        (title, body, image_url)
    VALUES
        (%(title)s, %(body)s, %(image_url)s)
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
