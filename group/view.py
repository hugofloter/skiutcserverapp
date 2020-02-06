from group.model import Group, UserGroup
from user.model import User
from user.view import UserView
from db import dbskiutc_con as db
from utils.errors import Error
from datetime import datetime
from notifications.view import NotificationsView
from notifications.model import NotificationMessage
import pymysql


class GroupView():
    def __init__(self, login=None):
        self.con = db()
        self.login = login

    def get_member(self, group_id):
        try:
            with self.con:
                cur = self.con.cursor(Model = UserGroup)
                sql = "SELECT * FROM usergroup WHERE id_group=%s AND login_user=%s"
                cur.execute(sql, (group_id, self.login))
                result=  cur.fetchone()

                if result is None:
                    raise Error('Unauthorized', 403)
                return result

        except Exception as e:
            raise e
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
                self.add_to_group(last.to_json().get('id'), login_list=list_login, group=last.to_json())
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
                sql = "SELECT * FROM `groups` WHERE id=%s"
                cur.execute(sql, id_group)

                group = cur.fetchone()
                if group is None:
                    return Error('Not Found', 404).get_error()
                if group.to_json()['owner'] == login:
                    sql = "DELETE FROM `groups` WHERE id = %s AND owner=%s"
                    cur.execute(sql, (id_group,  login))
                    if cur.rowcount == 0:
                        return Error('User unauthorized to delete this group', 403).get_error()
                    self.con.commit()
                else:
                    return self.remove_from_group(id_group, login)

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
    def add_to_group(self, id_group, login_list=None, owner=None, group=None):
        result = {}
        count = 0
        try:
            with self.con:

                if group is None:
                    group = self.get_global(id_group)

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

                        except Exception as e:
                            print(e)
                            code, message = e.args
                            if code == pymysql.constants.ER.DUP_ENTRY:
                                result[count] = {'error': message}
                                count += 1
                            else:
                                self.con.rollback()
                                raise e

                    tokens = UserView().list_tokens_from_logins(login_list)
                    message = NotificationMessage({
                        'title': 'Invitation de groupe - {}'.format(group.get('name')),
                        'text': '{} t\'a invité à rejoindre son nouveau groupe !'.format(group.get('owner'))
                        })
                    NotificationsView(message, tokens).send_push_message()

        except Exception as e:
            print(e)
            return Error('Problem happened when adding to group', 400).get_error()

        return result

    def list_user_from_group(self, id_group, accept_only=False):
        try:
            with self.con:
                cur = self.con.cursor(Model = UserGroup)
                accept_sql = f"AND `status`= 'V'" if accept_only else ""
                sql = f"SELECT * from `usergroup` WHERE `id_group` = %s {accept_sql}"
                cur.execute(sql, id_group)
                users_group = cur.fetchall()
                ug_dict = {}
                login_list = []
                for user in users_group:
                    user = user.to_json()
                    ug_dict[user['login_user']] = user
                    login_list.append(user['login_user'])

                users = UserView().list(list=login_list)
                for user_key in users:
                    user = users[user_key]
                    user_group = ug_dict.get(user['login'])

                    user['status'] = user_group['status']
                    user['expiration_date'] = user_group['expiration_date']

                    if user_group['share_position']:
                        user['location'] = UserView(user['login']).get_location()

                    users[user_key] = user

                return users

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
                list_users = self.list_user_from_group(id_group)

                group = response.to_json()
                group['users'] = list_users

                usergroup = self.get_member(id_group).to_json()
                group['share_position'] = usergroup.get('share_position')

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
    def remove_from_group(self, id_group, login, owner=None):
        try:
            with self.con:
                cur = self.con.cursor(Model = UserGroup)

                if owner:
                    if owner == login:
                        return Error('Can not delete from your own group', 400).get_error()
                    sql = "SELECT * FROM `groups` WHERE id=%s AND owner=%s"
                    cur.execute(sql, (id_group, owner))

                    group = cur.fetchone()
                    if group is None:
                        return Error('Not Found', 404).get_error()

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
    def handle_invitation(self, id_group, login, invitation_type):
        try:
            if invitation_type == 'V':
                with self.con:
                    cur = self.con.cursor(Model = UserGroup)
                    sql = "UPDATE `usergroup` SET status = 'V' WHERE `id_group` = %s AND `login_user` = %s"
                    cur.execute(sql, (id_group, login))
                    self.con.commit()
                    group = self.get_global(id_group)
                    group['user_status'] = 'V'

                    return self.list(login)
            else:
                with self.con:
                    cur = self.con.cursor(Model=UserGroup)
                    sql = "DELETE FROM `usergroup` WHERE `id_group` = %s AND `login_user` = %s"
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
    def new_beer_call(self, id_group, data):
        try:
            title = data.get('title')
            text = data.get('message')
            new_beer_call = datetime.now()
            last_beer_call = datetime.strptime(self.get_global(id_group).get('beer_call'), '%m-%d-%Y %H:%M:%S')
            if last_beer_call:
                time_diff = new_beer_call - last_beer_call
                if time_diff.seconds < 3600:
                    return Error('Not allowed to send notification, delay not great', 403).get_error()
            new_beer_call = new_beer_call.strftime('%Y-%m-%d %H:%M:%S')
            with self.con:
                cur = self.con.cursor(Model = UserGroup)
                sql = "UPDATE `groups` SET `beer_call` = %s WHERE id = %s"
                cur.execute(sql, (new_beer_call, id_group))
                self.con.commit()
                list_users = self.list_user_from_group(id_group)
                login_list = []
                for nb, user in list_users.items():
                    login_list.append(user.get('login'))
                tokens = UserView().list_tokens_from_logins(login_list)
                message = NotificationMessage({'title': title,
                                               'text': text})
                NotificationsView(message, tokens).send_push_message()

                return self.get(id_group)

        except Exception as e:
            print(e)
            self.con.rollback()
            return Error('Problem happened in updating user beer call in group', 400).get_error()

    """
    Update location permission of user
    :param id_group
    :param login
    """
    def update_permission_location(self, id_group, login, perm):
        try:
            with self.con:
                cur = self.con.cursor(Model = UserGroup)
                sql = "UPDATE `usergroup` SET `share_position` = %s WHERE `login_user` = %s AND `id_group` = %s"
                cur.execute(sql, (perm, login, id_group))
                self.con.commit()

                return self.get(id_group)


        except Exception as e:
            print(e)
            self.con.rollback()
            return Error('Problem happened in updating permission location for user', 400).get_error()
