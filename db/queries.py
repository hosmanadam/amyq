read_questions_for_search = """
    SELECT
        question.id,
        question.title,
        question.created,
        question.last_updated,
        question.body,
        user.username,
        ANY_VALUE(IFNULL(views.count, 0)) AS view_count,
        ANY_VALUE(IFNULL(votes.count, 0)) AS vote_count

    FROM
        question

        JOIN user ON question.user_id = user.id

        LEFT JOIN answer ON question.id = answer.question_id

        LEFT JOIN (
            SELECT
                question_id,
                SUM(count) AS count
            FROM view
            GROUP BY question_id
        ) AS views ON question.id = views.question_id

        LEFT JOIN (
            SELECT
                question_id,
                SUM(value) AS count
            FROM vote
            GROUP BY question_id
        ) AS votes ON question.id = votes.question_id

    WHERE
        question.title LIKE CONCAT('%', %(search)s, '%') OR
        question.body LIKE CONCAT('%', %(search)s, '%') OR
        answer.body LIKE CONCAT('%', %(search)s, '%')

    GROUP BY
        question.id
"""

read_question = """
    SELECT
        question.id,
        question.title,
        question.body,
        question.created,
        question.last_updated,
        user.username,
        ANY_VALUE(IFNULL(views.count, 0)) AS view_count,
        ANY_VALUE(IFNULL(votes.count, 0)) AS vote_count

    FROM
        question

        JOIN user ON question.user_id = user.id

        LEFT JOIN answer ON question.id = answer.question_id

        LEFT JOIN (
            SELECT
                question_id,
                SUM(count) AS count
            FROM view
            GROUP BY question_id
        ) AS views ON question.id = views.question_id

        LEFT JOIN (
            SELECT
                question_id,
                SUM(value) AS count
            FROM vote
            GROUP BY question_id
        ) AS votes ON question.id = votes.question_id

    WHERE
        question.id = %(id)s

    GROUP BY
        question.id
"""

read_answers = """
    SELECT * FROM answer
    WHERE question_id = %(id)s
    ORDER BY created DESC
"""

read_answer = """
    SELECT * FROM answer
    WHERE id = %(id)s
"""

read_comment = """
    SELECT * FROM comment
    WHERE id = %(id)s
"""

read_existing_tags = """
    SELECT * FROM tag
"""

read_tags_for_question = """
    SELECT tag.name, tag.id
    FROM tag JOIN tag_to_question ON tag.id = tag_to_question.tag_id
    WHERE question_id = %(question_id)s
    ORDER BY tag.name
"""

read_tag_id_for_tag_name = """
    SELECT id FROM tag
    WHERE name=%(name)s
"""

read_comments_for_question = """
    SELECT * FROM comment
    WHERE question_id = %(question_id)s
    ORDER BY created DESC
"""

read_comments_for_answer = """
    SELECT * FROM comment
    WHERE answer_id = %(answer_id)s
    ORDER BY created DESC
"""

read_latest_content_match_id = """
    SELECT id FROM question
    WHERE title = %(title)s
    ORDER BY created DESC
    LIMIT 1
"""

read_question_id_for_answer_id = """
    SELECT question_id FROM answer
    WHERE id = %(id)s
"""

add_question = """
    INSERT INTO question
        (title, body, image_url)
    VALUES
        (%(title)s, %(body)s, %(image_url)s)
"""

add_new_tag = """
    INSERT INTO tag
        (name)
    VALUES
        (%(name)s)
"""

add_existing_tag_to_question = """
    INSERT INTO tag_to_question
        (question_id, tag_id)
    VALUES
        (%(question_id)s, %(tag_id)s)
"""

add_answer = """
    INSERT INTO answer
        (question_id, body, image_url)
    VALUES
        (%(question_id)s, %(body)s, %(image_url)s)
"""

add_question_comment = """
    INSERT INTO comment
        (question_id, body)
    VALUES
        (%(question_id)s, %(body)s)
"""

add_answer_comment = """
    INSERT INTO comment
        (answer_id, body)
    VALUES
        (%(answer_id)s, %(body)s)
"""

update_question = """
    UPDATE question
    SET title=%(title)s, body=%(body)s, image_url=%(image_url)s
    WHERE id=%(id)s
"""

update_answer = """
    UPDATE answer
    SET body=%(body)s, image_url=%(image_url)s
    WHERE id=%(id)s
"""

update_comment = """
    UPDATE comment
    SET body=%(body)s
    WHERE id=%(id)s
"""

update_question_vote_count = """
    UPDATE question
    SET vote_count = vote_count + %(value)s
    WHERE id = %(id)s
"""

update_answer_vote_count = """
    UPDATE answer
    SET vote_count = vote_count + %(value)s
    WHERE id = %(id)s
"""

increment_question_view_count = """
    UPDATE question
    SET view_count = view_count + 1
    WHERE id = %(id)s
"""

delete_question = """
    DELETE FROM question
    WHERE id = %(id)s
"""

delete_tag_from_question = """
    DELETE FROM tag_to_question
    WHERE question_id = %(question_id)s AND tag_id = %(tag_id)s
"""

delete_answer = """
    DELETE FROM answer
    WHERE id = %(id)s
"""

delete_comment = """
    DELETE FROM comment
    WHERE id = %(id)s
"""
