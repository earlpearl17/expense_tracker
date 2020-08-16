# project/test.py


import os
import unittest

from views import app, db
from _config import basedir
from models import User

TEST_DB = 'test.db'


class AllTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()

    # executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    ########################
    #### helper methods ####
    ########################
    def login(self, name, password):
        return self.app.post('/', data=dict(
            name=name, password=password), follow_redirects=True)
            
    def register(self, name, email, password, confirm):
        return self.app.post(
            'register/',
            data=dict(name=name, email=email, password=password, confirm=confirm),
            follow_redirects=True
        )

    def logout(self):
        return self.app.get('logout/', follow_redirects=True)

    def create_user(self, name, email, password):
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

    def create_expense(self):
        return self.app.post('add/', data=dict(
            month='January',
            name='Big tasty pizza',
            amount='25.75'
        ), follow_redirects=True)    

    # def update_expense(self):
    #     return self.app.post('add/', data=dict(
    #         month='January',
    #         name='Big tasty pizza',
    #         amount=''
    #     ), follow_redirects=True)
    def create_admin_user(self):
        new_user = User(
            name='Superman',
            email='admin@realpython.com',
            password='allpowerful',
            role='admin'
        )
        db.session.add(new_user)
        db.session.commit()

    ###############
    #### tests ####
    ###############
    def test_users_can_register(self):
        new_user = User("michael", "michael@mherman.org", "michaelherman")
        db.session.add(new_user)
        db.session.commit()
        test = db.session.query(User).all()
        for t in test:
            t.name
        assert t.name == "michael"     
    
    def test_form_is_present_on_login_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please sign in to access your expense list', response.data)

    def test_users_cannot_login_unless_registered(self):
        response = self.login('foo', 'bar')
        self.assertIn(b'Invalid username or password.', response.data)    

    def test_users_can_login(self):
        self.register('Michael', 'michael@realpython.com', 'python', 'python')
        response = self.login('Michael', 'python')
        self.assertIn(b'Welcome!', response.data)
        
    def test_invalid_form_data(self):
        self.register('Michael', 'michael@realpython.com', 'python', 'python')
        response = self.login('alert("alert box!");', 'foo')
        self.assertIn(b'Invalid username or password.', response.data)
        
    def test_form_is_present_on_register_page(self):
        response = self.app.get('register/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please register to access your expense list', response.data)

    def test_user_registration(self):
        self.app.get('register/', follow_redirects=True)
        response = self.register(
            'Michael', 'michael@realpython.com', 'python', 'python')
        self.assertIn(b'Thanks for registering. Please login.', response.data)                    

    def test_user_registration_error(self):
        self.app.get('register/', follow_redirects=True)
        self.register('Michael', 'michael@realpython.com', 'python', 'python')
        self.app.get('register/', follow_redirects=True)
        response = self.register(
            'Michael', 'michael@realpython.com', 'python', 'python'
        )
        self.assertIn(
            b'That username and/or email already exist.',
            response.data
        )    

    def test_logged_in_users_can_logout(self):
        self.register('Fletcher', 'fletcher@realpython.com', 'python101', 'python101')
        self.login('Fletcher', 'python101')
        response = self.logout()
        self.assertIn(b'Goodbye!', response.data)    

    def test_not_logged_in_users_cannot_logout(self):
        response = self.logout()
        self.assertNotIn(b'Goodbye!', response.data)    

    def test_logged_in_users_can_access_expenses_page(self):
        self.register(
            'Fletcher', 'fletcher@realpython.com', 'python101', 'python101'
        )
        self.login('Fletcher', 'python101')
        response = self.app.get('expenses/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add a new expense:', response.data)

    def test_not_logged_in_users_cannot_access_expenses_page(self):
        response = self.app.get('expenses/', follow_redirects=True)
        self.assertIn(b'You need to login first.', response.data)    

    def test_users_can_add_expenses(self):
        self.create_user('Michael', 'michael@realpython.com', 'python')
        self.login('Michael', 'python')
        self.app.get('expenses/', follow_redirects=True)
        response = self.create_expense()
        self.assertIn(
            b'New expense was successfully added.', response.data
        )

    def test_users_cannot_add_expenses_when_error(self):
        self.create_user('Michael', 'michael@realpython.com', 'python')
        self.login('Michael', 'python')
        self.app.get('expenses/', follow_redirects=True)
        response = self.app.post('add/', data=dict(
            month='March',
            name='Gym membership',
            amount=''
        ), follow_redirects=True)
        self.assertIn(b'This field is required.', response.data)    

    def test_users_can_update_expenses(self):
        self.create_user('Michael', 'michael@realpython.com', 'python')
        self.login('Michael', 'python')
        self.app.get('expenses/', follow_redirects=True)
        self.create_expense()
        response = self.app.get("update/1/", follow_redirects=True)
        self.assertIn(b'Update an existing expense:', response.data)
        response = self.app.post('update/1/', data=dict(
            month='March',
            name='Gym membership',
            amount='15.00'
        ), follow_redirects=True)        
        self.assertIn(b'The expense was successfully updated.', response.data)

    def test_users_cannot_update_expenses_when_error(self):
        self.create_user('Michael', 'michael@realpython.com', 'python')
        self.login('Michael', 'python')
        self.app.get('expenses/', follow_redirects=True)
        self.create_expense()
        response = self.app.get("update/1/", follow_redirects=True)
        self.assertIn(b'Update an existing expense:', response.data)
        response = self.app.post('update/1/', data=dict(
              month='March',
              name='Gym membership',
              amount=''
        ), follow_redirects=True) 
        self.assertIn(b'This field is required.', response.data)    

    def test_users_can_delete_expenses(self):
        self.create_user('Michael', 'michael@realpython.com', 'python')
        self.login('Michael', 'python')
        self.app.get('expenses/', follow_redirects=True)
        self.create_expense()
        response = self.app.get("delete/1/", follow_redirects=True)
        self.assertIn(b'The expense was successfully deleted.', response.data)    

    def test_users_cannot_update_expenses_that_are_not_created_by_them(self):
        self.create_user('Michael', 'michael@realpython.com', 'python')
        self.login('Michael', 'python')
        self.app.get('expenses/', follow_redirects=True)
        self.create_expense()
        self.logout()
        self.create_user('Fletcher', 'fletcher@realpython.com', 'python101')
        self.login('Fletcher', 'python101')
        self.app.get('expenses/', follow_redirects=True)
        response = self.app.get("update/1/", follow_redirects=True)
        self.assertNotIn(
            b'Update an existing expense:', response.data
        )  
        self.assertIn(
            b'You can only update expenses that belong to you.', response.data
        )

    def test_users_cannot_delete_expenses_that_are_not_created_by_them(self):
        self.create_user('Michael', 'michael@realpython.com', 'python')
        self.login('Michael', 'python')
        self.app.get('expenses/', follow_redirects=True)
        self.create_expense()
        self.logout()
        self.create_user('Fletcher', 'fletcher@realpython.com', 'python101')
        self.login('Fletcher', 'python101')
        self.app.get('expenses/', follow_redirects=True)
        response = self.app.get("delete/1/", follow_redirects=True)
        self.assertIn(
            b'You can only delete expenses that belong to you.', response.data
        )

    def test_default_user_role(self):

        db.session.add(
            User(
                "Johnny",
                "john@doe.com",
                "johnny"
            )
        )

        db.session.commit()

        users = db.session.query(User).all()
        for user in users:
            self.assertEqual(user.role, 'user') 

    def test_admin_users_can_update_expenses_that_are_not_created_by_them(self):
        self.create_user('Michael', 'michael@realpython.com', 'python')
        self.login('Michael', 'python')
        self.app.get('expenses/', follow_redirects=True)
        self.create_expense()
        self.logout()
        self.create_admin_user()
        self.login('Superman', 'allpowerful')
        self.app.get('expenses/', follow_redirects=True)
        response = self.app.get("update/1/", follow_redirects=True)
        # self.assertIn(b'Update an existing expense:', response.data)
        # response = self.app.post('update/1/', data=dict(
        #     month='March',
        #     name='Gym membership',
        #     amount='15.00'
        # ), follow_redirects=True)        
        #self.assertIn(b'The expense was successfully updated.', response.data)
        self.assertNotIn(
            b'You can only update expenses that belong to you.', response.data
        )

    def test_admin_users_can_delete_expenses_that_are_not_created_by_them(self):
        self.create_user('Michael', 'michael@realpython.com', 'python')
        self.login('Michael', 'python')
        self.app.get('expenses/', follow_redirects=True)
        self.create_expense()
        self.logout()
        self.create_admin_user()
        self.login('Superman', 'allpowerful')
        self.app.get('expenses/', follow_redirects=True)
        response = self.app.get("delete/1/", follow_redirects=True)
        self.assertNotIn(
            b'You can only delete tasks that belong to you.', response.data
        )

    # def test_string_reprsentation_of_the_task_object(self):

    #     from datetime import date
    #     db.session.add(
    #         Task(
    #             "Run around in circles",
    #             date(2015, 1, 22),
    #             10,
    #             date(2015, 1, 23),
    #             1,
    #             1
    #         )
    #     )

    #     db.session.commit()

    #     tasks = db.session.query(Task).all()
    #     for task in tasks:
    #         self.assertEqual(task.name, 'Run around in circles')    


if __name__ == "__main__":
    unittest.main()        