read_info_for_all_users = """
    SELECT * FROM user
"""

read_questions_by_user = """
    SELECT
        question.id,
        question.title,
        question.created,
        question.last_updated,
        question.body,
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
        user.username = %(username)s

    GROUP BY
        question.id
"""

read_answers_by_user = """
    SELECT
        answer.id,
        answer.body,
        answer.image_url,
        answer.created,
        answer.last_updated,
        ANY_VALUE(IFNULL(votes.count, 0)) AS vote_count,
        answer.question_id

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
        user.username = %(username)s

    GROUP BY
        answer.id
"""

read_comments_by_user = """
    SELECT
        comment.id,
        comment.body,
        comment.created,
        IFNULL(comment.question_id, answer.question_id) AS question_id,
        comment.answer_id
    FROM
        comment
        JOIN user ON comment.user_id = user.id
        LEFT JOIN answer ON comment.answer_id = answer.id
    WHERE
        user.username = %(username)s
"""

read_questions_for_search = """
    SELECT
        question.id,
        question.title,
        question.created,
        question.last_updated,
        question.body,
        user.id AS user_id,
        user.username,
        user.first_name,
        user.last_name,
        user.locality,
        user.country,
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
        question.accepted_answer_id,
        user.id AS user_id,
        user.username,
        user.first_name,
        user.last_name,
        user.locality,
        user.country,
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
        user.id AS user_id,
        user.username,
        user.first_name,
        user.last_name,
        user.locality,
        user.country,
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

read_comments_for_question = """
    SELECT
        comment.id,
        comment.body,
        comment.created,
        comment.last_updated,
        user.id AS user_id,
        user.username,
        user.first_name,
        user.last_name,
        user.locality,
        user.country
    FROM
        comment
        JOIN user ON comment.user_id = user.id
    WHERE
        comment.question_id = %(question_id)s
"""

read_comments_for_answer = """
    SELECT
        comment.id,
        comment.body,
        comment.created,
        comment.last_updated,
        user.id AS user_id,
        user.username,
        user.first_name,
        user.last_name,
        user.locality,
        user.country
    FROM
        comment
        JOIN user ON comment.user_id = user.id
    WHERE
        comment.answer_id = %(answer_id)s
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

read_user_info_for_username = """
    SELECT * FROM user
    WHERE username = %(username)s
"""

# TODO: test
read_user_reputation = """
SELECT

    IFNULL(reputation_from_question_votes, 0) AS reputation_from_question_votes,
    IFNULL(reputation_from_answer_votes, 0) AS reputation_from_answer_votes,
    IFNULL(reputation_from_answer_accepts, 0) AS reputation_from_answer_accepts,
    IFNULL((reputation_from_question_votes +
            reputation_from_answer_votes +
            reputation_from_answer_accepts), 0) AS reputation_total

FROM

  (SELECT SUM(IF(value=1, 5, 0) + IF(value=-1, -2, 0)) AS reputation_from_question_votes
  FROM question
  LEFT JOIN vote ON question.id = vote.question_id
  WHERE question.user_id = %(user_id)s) AS question_vote_aggregate

JOIN

  (SELECT SUM(IF(value=1, 10, 0) + IF(value=-1, -2, 0)) AS reputation_from_answer_votes
  FROM answer
  LEFT JOIN vote ON answer.id = vote.answer_id
  WHERE answer.user_id = %(user_id)s) AS answer_vote_aggregate

JOIN

  (SELECT SUM(15) AS reputation_from_answer_accepts
  FROM question
  JOIN answer on question.accepted_answer_id = answer.id
  WHERE answer.user_id = %(user_id)s) AS answer_accept_aggregate
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

update_accepted_answer = """
    UPDATE question
    SET accepted_answer_id = %(answer_id)s
    WHERE id = %(id)s
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
