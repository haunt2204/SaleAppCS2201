from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import Category, Product
from saleapp import app, db


admin = Admin(app, name="E-commerce Website", template_mode="bootstrap4")


class MyCategoryView(ModelView):
    column_list = ['name', 'products']
    column_searchable_list = ['id', 'name']


class MyProductView(ModelView):
    column_searchable_list = ['id', 'name']
    column_filters = ['id', 'name']

admin.add_view(MyCategoryView(Category, db.session))
admin.add_view(MyProductView(Product, db.session))