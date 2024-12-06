from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from saleapp import app, db
from models import Category, Product


admin = Admin(app=app, name="E-commerce Website", template_mode="bootstrap4")


class MyCategoryView(ModelView):
    column_list = ["name", "products"]


class MyProductView(ModelView):
    column_list = ["name", "category_id", "image"]
    column_searchable_list = ["id", "name"]
    column_filters = ["id", "name"]
    can_export = True


admin.add_views(MyCategoryView(Category, db.session))
admin.add_views(MyProductView(Product, db.session))