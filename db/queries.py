read_questions = """
    SELECT * FROM questions
    ORDER BY time_submitted DESC
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

read_latest_content_match_id = """
    SELECT id FROM questions
    WHERE title = %(title)s
    ORDER BY time_submitted DESC
    LIMIT 1
"""
