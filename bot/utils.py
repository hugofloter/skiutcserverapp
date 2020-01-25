import json
from bot.view import BotView
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
            for answer in answers:
                cur = con.cursor(Model=BotAnswer)
                score = answer.get('score')
                response = answer.get('response')
                sql = "INSERT INTO `bot_answer` (`question_id`, `response`, `score`) VALUES (%s)"
                cur.execute(sql, (question.to_json.get('id'), response, score))
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
        id_question = question.to_json.get('id')
        with con:
            cur = con.cursor(Model=BotAnswer)
            sql = "SELECT * FROM `bot_answer` WHERE `question_id` = %s"
            cur.execute(sql, id_question)
            list_answers = cur.fetchall()
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


def send_question():
    return None

def send_all_question():
    return None
