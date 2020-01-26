import json
from bot.model import BotQuestion, BotAnswer, UserAnswer
from db import dbskiutc_con as db


def create_question(data):
    con = db()
    try:
        question = data.get('question')
        answers = data.get('answers')
        with con:
            cur = con.cursor(Model=BotQuestion)
            sql = "INSERT INTO `bot_question` (`question`) VALUES (%s)"
            cur.execute(sql, question)
            sql = "SELECT * FROM `bot_question` WHERE id = (SELECT MAX(id) FROM `bot_question`)"
            cur.execute(sql)
            question = cur.fetchone()

            cur = con.cursor(Model=BotAnswer)
            for answer in answers:
                score = answer.get('score')
                response = answer.get('response')
                print(response)
                print(score)
                sql = "INSERT INTO `bot_answer` (`question_id`, `response`, `score`) VALUES (%s, %s, %s)"
                cur.execute(sql, (int(question.to_json().get('id')), response, score))
            con.commit()

        return list_answers_from_question(question)

    except Exception as e:
        print(e)
        con.rollback()
        return e


def list_answers_from_question(question):
    con = db()
    count = 0
    result = {}
    try:
        question = question.to_json()
        id_question = question.get('id')
        with con:
            cur = con.cursor(Model=BotAnswer)
            sql = "SELECT * FROM `bot_answer` WHERE `question_id` = %s"
            cur.execute(sql, id_question)
            list_answers = cur.fetchall()
            if not list_answers or not len(list_answers):
                return question

            for answer in list_answers:
                current = answer.to_json()
                result[count] = current
                count += 1
            question['answers'] = result
            return question
    except Exception as e:
        print(e)
        con.rollback()
        return e


def add_answer(data):
    con = db()
    try:
        a_id = data.get('a_id')
        q_id = data.get('q_id')
        login = data.get('login')
        cur = con.cursor(Model = UserAnswer)
        sql = "SELECT * FROM user_answer WHERE login=%s AND question_id=%s"
        cur.execute(sql, (login, q_id))
        user = cur.fetchone()
        if user:
            return None
        sql = "INSERT INTO user_answer (login, question_id, answer_id) VALUES (%s, %s, %s)"
        cur.execute(sql, (login, q_id, a_id))
        con.commit()

        return answers_stats(q_id)

    except Exception as e:
        print(e)
        con.rollback()


def answers_stats(q_id):
    con = db()
    try:
        cur = con.cursor(Model = BotQuestion)
        sql = "SELECT * FROM bot_question WHERE id=%s"
        cur.execute(sql, q_id)

        question = cur.fetchone()
        if question is None:
            return None

        list_answers = list_answers_from_question(question)
        list_answers = list_answers.get('answers')

        cur = con.cursor(Model = UserAnswer)
        sql = "SELECT * FROM `user_answer` WHERE question_id=%s"
        cur.execute(sql, q_id)

        answers = cur.fetchall()
        length = len(answers)
        stats = {}

        for key in list_answers:
            answer = list_answers[key]
            stats[answer.get('id')] = {
                'response': answer.get('response')
            }

        for answer in answers:
            answer = answer.to_json()
            stats[answer.get('answer_id')]['stats'] = round(float(stats[answer.get('answer_id')].get('stats', 0) + 1/length), 2)

        return stats

    except Exception as e:
        print(e)


def send_question():
    con = db()
    try:
        cur = con.cursor(Model=BotQuestion)
        sql = "SELECT * FROM bot_question WHERE sent=0 ORDER BY RAND() LIMIT 1"
        cur.execute(sql)
        question = cur.fetchone()

        if question is None:
            return None
        return list_answers_from_question(question)

    except Exception as e:
        print(e)


def list_question():
    con = db()
    count = 0
    result = {}
    try:
        with con:
            cur = con.cursor(Model=BotQuestion)
            sql = "SELECT * FROM `bot_question`"
            cur.execute(sql)
            list_q = cur.fetchall()
            if not list_q or not len(list_q):
                return None
            for question in list_q:
                current = question.to_json()
                result[count] = current
                count += 1
            return result

    except Exception as e:
        print(e)
        con.rollback()
        return e


def send_all_question():
    return None
