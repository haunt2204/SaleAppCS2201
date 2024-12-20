from flask_admin import Admin, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView
from saleapp import app, db
from models import Category, Product, UserEnum
from flask_login import current_user, logout_user
from flask import redirect


admin = Admin(app=app, name="E-commerce Website", template_mode="bootstrap4")


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == UserEnum.ADMIN


class MyCategoryView(MyModelView):
    column_list = ["name", "products"]


class MyProductView(MyModelView):
    column_list = ["name", "category_id", "image"]
    column_searchable_list = ["id", "name"]
    column_filters = ["id", "name"]
    can_export = True


class MyBaseView(BaseView):

    def is_accessible(self):
        return current_user.is_authenticated


class StatsView(MyBaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')


class LogoutView(MyBaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


admin.add_views(MyCategoryView(Category, db.session))
admin.add_views(MyProductView(Product, db.session))
admin.add_views(StatsView(name="Thống kê"))
admin.add_views(LogoutView(name="Đăng xuất"))