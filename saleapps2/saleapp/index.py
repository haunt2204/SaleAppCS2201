import math
from flask_login import login_user, current_user, logout_user, login_required
from flask import render_template, request, redirect, session, jsonify
import dao, utils
from saleapp import app, admin, login
import cloudinary.uploader


@app.route('/')
def index():
    q = request.args.get("q")
    cate_id = request.args.get("category_id")
    page = request.args.get("page")
    products = dao.load_products(q=q, cate_id=cate_id, page=page)
    pages = dao.count_product()
    return render_template('index.html', products=products, pages=math.ceil(pages/app.config["PAGE_SIZE"]))


@app.route('/products/<int:id>')
def details(id):
    product = dao.load_product_by_id(id)
    return render_template('product-details.html', product = product)


@app.route('/register', methods=["get", "post"])
def register_user():
    err_msg = None
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        if password.__eq__(confirm):
            ava_path = None
            name = request.form.get('name')
            username = request.form.get('username')
            avatar = request.files.get('avatar')
            if avatar:
                res = cloudinary.uploader.upload(avatar)
                ava_path = res['secure_url']
            dao.add_user(name=name, username=username, password=password, avatar=ava_path)
            return redirect('/login')
        else:
            err_msg = "Mật khẩu không khớp!"
    return render_template('register.html', err_msg=err_msg)

@app.route('/login', methods=['get', 'post'])
def login_my_user():
    if current_user.is_authenticated:
        return redirect("/")
    err_msg = None
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user)
            next = request.args.get('next')
            return redirect(next if next else '/')
        else:
            err_msg = "Tài khoản hoặc mật khẩu không đúng!"

    return render_template('login.html', err_msg=err_msg)


@app.route('/login-admin', methods=['post'])
def process_login_admin():
    username = request.form.get('username')
    password = request.form.get('password')
    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user)
    else:
        err_msg = "Tài khoản hoặc mật khẩu không đúng!"

    return redirect('/admin')


@app.route('/logout')
def logout_my_user():
    logout_user()
    return redirect('/login')


@app.context_processor
def common_attributes():
    return {
        "categories": dao.load_categories(),
        "stats_cart": utils.count_cart(session.get('cart'))
    }


@app.route('/cart')
def cart():
    return render_template('cart.html')

@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id=user_id)


@app.route("/api/pay", methods=['post'])
@login_required
def pay():
    cart = session['cart']
    try:
        dao.add_receipt(cart=cart)
    except Exception as ex:
        print(ex)
        return jsonify({'status': 500})
    else:
        del session['cart']
        return jsonify({'status': 200})


@app.route('/api/products/<int:id>/comments', methods=['post'])
@login_required
def add_comment(id):
    data = request.json
    c = dao.add_comment(content=data.get('content'), product_id=id)

    return jsonify({'id': c.id, 'content': c.content, 'product_id': c.product_id, 'user': {
        'username': c.user.username,
        'avatar': c.user.avatar
    }})

@app.route('/api/cart/<prod_id>', methods=['put'])
def update_cart(prod_id):
    cart = session.get('cart')
    if cart and prod_id in cart:
        cart[prod_id]['quantity'] = request.json['quantity']
        session['cart'] = cart
    return jsonify(utils.count_cart(cart))


@app.route('/api/cart/<prod_id>', methods=['delete'])
def delete_cart(prod_id):
    cart = session.get('cart')
    if cart and prod_id in cart:
        del cart[prod_id]
        session['cart'] = cart
    return jsonify(utils.count_cart(cart))


@app.route('/api/carts', methods=['post'])
def add_to_cart():
    """
    {
        "cart": {
        "1": {
            "id": "",
            "name": "",
            "price": "2000",
            "quantity": 2
        },
        "2": {
            "id": "",
            "name": "",
            "price": "",
            "quantity": 1
        }
    }
    }
    :return:
    """

    cart = session.get("cart")

    if not cart:
        cart = {}

    id = str(request.json.get('id'))

    if id in cart:
        cart[id]["quantity"] += 1
    else:
        cart[id] = {
            "id": id,
            "name": request.json.get('name'),
            "price": request.json.get('price'),
            "quantity": 1
        }

    session['cart'] = cart

    return jsonify(utils.count_cart(cart))

if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)