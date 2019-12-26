from group.model import Group, UserGroup
from db import dbskiutc_con as db


class GroupView():
    def __init__(self):
        self.con = db()

    """
    Create a group given datas model
    :param data
    """
    def create(self, data):
        try:
            with self.con:
                name = data.get('name')
                owner = data.get('owner')
                cur = self.con.cursor(Model = Group)
                sql = "INSERT INTO `groups` (name, owner) VALUES (%s, %s)"
                cur.execute(sql, (name, owner))
                self.con.commit()
                sql = "SELECT * FROM `groups` ORDER BY id DESC"
                cur.execute(sql)
                last = cur.fetchone()

                return last.to_json()

        except Exception as e:
            print(e)
            self.con.rollback()
            return e

    """
    :param id - id of group
    :param loginList list of login to add
    :return json list of user added to group on usergroup format
    """
    def add_to_group(self, id, loginList):
        result = {}
        count = 0
        for login in loginList:
            try:
                with self.con:
                    cur = self.con.cursor(Model = UserGroup)
                    sql = "INSERT INTO `usergroup` (`login_user`, `id_group`) VALUES (%s, %s)"
                    cur.execute(sql, (login, id))
                    self.con.commit()
                    sql = "SELECT * FROM `usergroup` WHERE `ìd_group` = %s AND `login_user` = %s"
                    cur.execute(sql, (id, login))
                    last = cur.fetchone()
                    result[count] = last
                    count += 1

            except Exception as e:
                print(e)
                self.con.rollback()
                return e
        return result

    def list_user_from_group(self, id):
        try:
            with self.con:
                cur = self.con.cursor(Model = UserGroup)
                sql = "SELECT * from `usergroup` WHERE `ìd_group` = %s"
                cur.execute(sql, id)
                response = cur.fetchall()
                count = 0
                result = {}
                for value in response:
                    usergroup = value.to_json()
                    result[count] = usergroup
                    count += 1

                return result

        except Exception as e:
            return e

    """
    get group from id
    """
    def get(self, id):
        try:
            with self.con:
                cur = self.con.cursor(Model = Group)
                sql = "SELECT * from `groups` WHERE id = %s"
                cur.execute(sql, id)
                response = cur.fetchone()
                if response is None:
                    return {}

                return response.to_json()

        except Exception as e:
            return e

    """
    get list group from login 
    """
    def list(self, login):
        try:
            with self.con:
                cur = self.con.cursor(Model = Group)
                sql = "SELECT * from `usergroup` WHERE `login_user` = %s"
                cur.execute(sql, login)
                response = cur.fetchall()
                if response is None:
                    return {}
                count = 0
                result = {}
                for u in response:
                    current = u.to_json()
                    group = self.get(current['id'])
                    result[count] = group
                    count += 1

                return result

        except Exception as e:
            return e

    """
    remove a user from a group - used when user decide to cancel invitation to group
    """
    def remove_from_group(self, id, login):
        try:
            with self.con:
                cur = self.con.cursor(Model = UserGroup)
                sql = "DELETE FROM `usergroup` WHERE id = %s AND login = %S"
                cur.execute(sql, (id, login))
                self.con.commit()

                return self.list(login)

        except Exception as e:
            return e

    """
    Update a group given an id
    :param id
    """
    def update_group(self, id):
        try:
            with self.con:
                cur = self.con.cursor(Model = Potin)
                sql = "UPDATE potin SET approved = 1 WHERE id = %s"
                cur.execute(sql, id)
                self.con.commit()

                return self.list()

        except Exception as e:
            self.con.rollback()
            return e

