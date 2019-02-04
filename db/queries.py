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
        question.image_url,
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
    SELECT
        answer.id,
        answer.body,
        answer.image_url,
        answer.created,
        answer.last_updated,
        user.username,
        ANY_VALUE(IFNULL(votes.count, 0)) AS vote_count

    FROM
        answer

        JOIN user ON answer.user_id = user.id

        LEFT JOIN (
            SELECT
                answer_id,
                SUM(value) AS count
            FROM vote
            GROUP BY answer_id
        ) AS votes ON answer.id = votes.answer_id

    WHERE
        answer.question_id = %(question_id)s

    GROUP BY
        answer.id
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
    SELECT tag.id, tag.name, tag.user_id
    FROM tag
"""

read_tags_for_question = """
    SELECT tag.id, tag.name, tag.user_id
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

read_password_hash_for_username = """
    SELECT password_hash
    FROM user
    WHERE username = %(username)s
"""

read_question_id_for_answer_id = """
    SELECT question_id FROM answer
    WHERE id = %(id)s
"""

add_question = """
    INSERT INTO question
        (user_id, title, body, image_url)
    VALUES
        (%(user_id)s, %(title)s, %(body)s, %(image_url)s)
"""

add_new_tag = """
    INSERT INTO tag
        (name, user_id)
    VALUES
        (%(name)s, %(user_id)s)
"""

add_existing_tag_to_question = """
    INSERT INTO tag_to_question
        (question_id, tag_id, user_id)
    VALUES
        (%(question_id)s, %(tag_id)s, %(user_id)s)
"""

add_answer = """
    INSERT INTO answer
        (user_id, question_id, body, image_url)
    VALUES
        (%(user_id)s, %(question_id)s, %(body)s, %(image_url)s)
"""

add_question_comment = """
    INSERT INTO comment
        (user_id, question_id, body)
    VALUES
        (%(user_id)s, %(question_id)s, %(body)s)
"""

add_answer_comment = """
    INSERT INTO comment
        (user_id, answer_id, body)
    VALUES
        (%(user_id)s, %(answer_id)s, %(body)s)
"""

add_user = """
    INSERT INTO user
        (username, password_hash, email, first_name, last_name, locality, country, facebook_username, github_username, twitter_username, linkedin_profile_url) 
    VALUES
        (%(username)s, %(password_hash)s, %(email)s, %(first_name)s, %(last_name)s, %(locality)s, %(country)s, %(facebook_username)s, %(github_username)s, %(twitter_username)s, %(linkedin_profile_url)s)
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
    INSERT INTO vote
        (user_id, question_id, value)
    VALUES
        (%(user_id)s, %(question_id)s, %(value)s)
    ON DUPLICATE KEY UPDATE value = %(value)s
"""

update_answer_vote_count = """
    INSERT INTO vote
        (user_id, answer_id, value)
    VALUES
        (%(user_id)s, %(answer_id)s, %(value)s)
    ON DUPLICATE KEY UPDATE value = %(value)s
"""

increment_question_view_count = """
    INSERT INTO view
        (user_id, question_id, count)
    VALUES
        (%(user_id)s, %(question_id)s, 1)
    ON DUPLICATE KEY UPDATE count =
        IF(
          TIMESTAMPDIFF(MINUTE, IFNULL(last_updated, created), NOW()) > 10,
          count+1,
          count);
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
