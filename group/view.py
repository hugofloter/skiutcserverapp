from group.model import Group, UserGroup
from user.model import User
from user.view import UserView
from db import dbskiutc_con as db
from utils.errors import Error
from datetime import datetime
import pymysql


class GroupView():
    def __init__(self):
        self.con = db()

    """
    Create a group given datas model
    :param name > string name of group
    :param owner >  string user login that created the group
    :param list_login > array of login to send invitation
    """
    def create(self, name, owner, list_login):
        try:
            with self.con:
                cur = self.con.cursor(Model = Group)
                sql = "INSERT INTO `groups` (name, owner) VALUES (%s, %s)"
                cur.execute(sql, (name, owner))
                sql = "SELECT * FROM `groups` WHERE id = (SELECT MAX(id) FROM `groups`)"
                cur.execute(sql)
                last = cur.fetchone()
                self.add_to_group(last.to_json().get('id'), owner=owner)
                self.add_to_group(last.to_json().get('id'), login_list=list_login)
                self.con.commit()
                return last.to_json()

        except Exception as e:
            print(e)
            self.con.rollback()
            return Error('Problem happened in group creation', 400).get_error()

    """
    delete a group given id
    :param data
    """
    def delete(self, id_group, login):
        try:
            with self.con:
                cur = self.con.cursor(Model = Group)
                sql = "DELETE FROM `groups` WHERE id = %s AND owner=%s"
                cur.execute(sql, (id_group,  login))
                if cur.rowcount == 0:
                    return Error('User unauthorized to delete this group', 403).get_error()
                self.con.commit()

                return self.list(login)

        except Exception as e:
            print(e)
            self.con.rollback()
            return Error('Problem happened in group deletion', 400).get_error()

    """
    :param id - id of group
    :param loginList list of login to add
    :return array list of user added to group on usergroup format
    """
    def add_to_group(self, id_group, login_list=None, owner=None):
        result = {}
        count = 0
        try:
            with self.con:
                if owner:
                    cur = self.con.cursor(Model=UserGroup)
                    sql = "INSERT INTO `usergroup` (`login_user`, `id_group`, `status`) VALUES (%s, %s, %s)"
                    cur.execute(sql, (owner, id_group, 'V'))
                    sql = "SELECT * FROM `usergroup` WHERE `id_group` = %s AND `login_user` = %s "
                    cur.execute(sql, (id_group, owner))
                    last = cur.fetchone()
                    result[count] = last.to_json()
                    count += 1
                if login_list:
                    for login in login_list:
                        try:
                            cur = self.con.cursor(Model=UserGroup)
                            sql = "INSERT INTO `usergroup` (`login_user`, `id_group`) VALUES (%s, %s)"
                            cur.execute(sql, (login, id_group))
                            sql = "SELECT * FROM `usergroup` WHERE `id_group` = %s AND `login_user` = %s"
                            cur.execute(sql, (id_group, login))
                            last = cur.fetchone()
                            result[count] = last.to_json()
                            count += 1
                            # @TODO use Notification here

                        except Exception as e:
                            print(e)
                            code, message = e.args
                            if code == pymysql.constants.ER.DUP_ENTRY:
                                result[count] = {'error': message}
                                count += 1
                            else:
                                self.con.rollback()
                                raise e

        except Exception as e:
            print(e)
            return Error('Problem happened when adding to group', 400).get_error()

        return result

    def list_user_from_group(self, id_group):
        try:
            with self.con:
                cur = self.con.cursor(Model = UserGroup)
                sql = "SELECT * from `usergroup` WHERE `id_group` = %s"
                cur.execute(sql, id_group)
                response = cur.fetchall()
                count = 0
                result = {}
                for value in response:
                    usergroup = value.to_json()
                    result[count] = usergroup
                    count += 1

                return result

        except Exception as e:
            print(e)
            return Error('Problem happened in query list', 400).get_error()

    """
    get group focus info from id
    """
    def get(self, id_group):
        try:
            with self.con:
                cur = self.con.cursor(Model = Group)
                sql = "SELECT * from `groups` WHERE id = %s"
                cur.execute(sql, id_group)
                response = cur.fetchone()
                if response is None:
                    return {}
                list_users = self.merge_user_location(id_group)

                group = response.to_json()
                group['users'] = list_users

                return group

        except Exception as e:
            print(e)
            return Error('Problem happened in query get', 400).get_error()

    """
    get group global info from id
    """
    def get_global(self, id_group):
        try:
            with self.con:
                cur = self.con.cursor(Model = Group)
                sql = "SELECT * from `groups` WHERE id = %s"
                cur.execute(sql, id_group)
                response = cur.fetchone()
                if response is None:
                    return {}

                return response.to_json()

        except Exception as e:
            print(e)
            return Error('Problem happened in query get', 400).get_error()

    """
    get list group from login 
    """
    def list(self, login):
        try:
            with self.con:
                cur = self.con.cursor(Model = UserGroup)
                sql = "SELECT * from `usergroup` WHERE `login_user` = %s"
                cur.execute(sql, login)
                response = cur.fetchall()
                if response is None:
                    return {}
                count = 0
                result = {}
                for u in response:
                    current = u.to_json()
                    group = self.get_global(current.get('id_group'))
                    group['user_status'] = current.get('status')
                    result[count] = group
                    count += 1

                return result

        except Exception as e:
            print(e)
            return Error('Problem happened in query list', 400).get_error()

    """
    remove a user from a group - used when user decide to avoid invitation to group
    """
    def remove_from_group(self, id_group, login):
        try:
            with self.con:
                cur = self.con.cursor(Model = UserGroup)
                sql = "DELETE FROM `usergroup` WHERE `id_group` = %s AND `login_user` = %s"
                cur.execute(sql, (id_group, login))
                self.con.commit()

                return self.list(login)

        except Exception as e:
            print(e)
            return Error('Problem happened in user deletion from group', 400).get_error()

    """
    Update a group given an id
    :param id
    """
    def accept_group(self, id_group, login):
        try:
            with self.con:
                cur = self.con.cursor(Model = UserGroup)
                sql = "UPDATE `usergroup` SET status = 'V' WHERE `id_group` = %s AND `login_user` = %s"
                cur.execute(sql, (id_group, login))
                self.con.commit()

                return self.list(login)

        except Exception as e:
            print(e)
            self.con.rollback()
            return Error('Problem happened in updating user status in group', 400).get_error()

    """
    Set a new beer call to group
    :param id
    """
    def new_beer_call(self, id_group):
        try:
            new_beer_call = datetime.now()
            new_beer_call = new_beer_call.strftime('%Y-%m-%d %H:%M:%S')
            with self.con:
                cur = self.con.cursor(Model = UserGroup)
                sql = "UPDATE `groups` SET `beer_call` = %s WHERE id = %s"
                cur.execute(sql, (new_beer_call, id_group))
                self.con.commit()
                #@TODO use Notification here

                return self.get(id_group)

        except Exception as e:
            print(e)
            self.con.rollback()
            return Error('Problem happened in updating user beer call in group', 400).get_error()

    """
    check if user allow location
    :param
    """
    def user_allow_location(self, id_group, login):
        try:
            with self.con:
                cur = self.con.cursor(Model = UserGroup)
                sql = "SELECT * from `usergroup` WHERE login_user = %s and id_group = %s"
                cur.execute(sql, (login, id_group))
                response = cur.fetchone()
                if response is None:
                    return False
                return bool(response.to_json().get('share_position'))

        except Exception as e:
            print(e)
            return Error('Problem happened in query get', 400).get_error()

    """
    Update location permission of user
    :param id_group
    :param login
    """
    def update_permission_location(self, id_group, login, perm):
        try:
            with self.con:
                cur = self.con.cursor(Model = User)
                sql = "UPDATE `usergroup` SET `share_position` = %s WHERE `login_user` = %s AND `id_group` = %s"
                cur.execute(sql, (perm, login, id_group))
                self.con.commit()

                return self.get(id_group)

        except Exception as e:
            print(e)
            self.con.rollback()
            return Error('Problem happened in updating permission location for user', 400).get_error()

    """
    Update location of user
    :param login
    :param location Location object 
    """
    def update_location(self, login, location, id_group):
        try:
            with self.con:
                cur = self.con.cursor(Model = User)
                sql = "UPDATE `users_app` SET `lastPosition` = POINT(%s, %s) WHERE login = %s"
                cur.execute(sql, (location.to_json().get('latitude'), location.to_json().get('longitude'), login))
                self.con.commit()

                return self.get(id_group)

        except Exception as e:
            print(e)
            self.con.rollback()
            return Error('Problem happened in updating location for user', 400).get_error()

    """
    list of location by user if allow
    :param id_group
    """
    def merge_user_location(self, id_group):
        try:
            list_users_in_group = self.list_user_from_group(id_group)
            for (n, user) in list_users_in_group.items():
                if user.get('share_position'):
                    location = UserView(user.get('login_user')).get_location()
                    user['location'] = location

            return list_users_in_group

        except Exception as e:
            print(e)
            return Error('Problem happened when merging location', 400).get_error()
