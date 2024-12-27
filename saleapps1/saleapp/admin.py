from flask import redirect
from flask_admin import Admin, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView
from models import Category, Product, UserEnum
from saleapp import app, db
from flask_login import logout_user, current_user


admin = Admin(app, name="E-commerce Website", template_mode="bootstrap4")

class BaseModelView(ModelView):
    def is_visible(self):
        return current_user.is_authenticated and current_user.role == UserEnum.ADMIN


class MyCategoryView(BaseModelView):
    column_list = ['name', 'products']
    column_searchable_list = ['id', 'name']


class MyProductView(BaseModelView):
    column_searchable_list = ['id', 'name']
    column_filters = ['id', 'name']


class MyStatsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')

    def is_visible(self):
        return current_user.is_authenticated and current_user.role == UserEnum.ADMIN


class AdminLogout(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


admin.add_view(MyCategoryView(Category, db.session))
admin.add_view(MyProductView(Product, db.session))
admin.add_view(MyStatsView("Thống kê"))
admin.add_view(AdminLogout("Đăng xuất"))