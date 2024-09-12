from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from db import db, Users, Fragrances

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.get_id() == '1'

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.get_id() == '1'
    
class UserView(MyModelView):
    column_exclude_list =['password']


admin = Admin(name='Administrator',index_view=MyAdminIndexView())
admin.add_view(UserView(Users,db.session))
admin.add_view(MyModelView(Fragrances,db.session))