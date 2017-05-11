from flask import Flask, render_template, request, json, session, redirect, url_for, escape, flash
from hashlib import md5
from flaskext.mysql import MySQL
import os

application = Flask(__name__)
mysql = MySQL()

# MySQL configurations
application.config['MYSQL_DATABASE_USER'] = 'trainer'
application.config['MYSQL_DATABASE_PASSWORD'] = 'trainer7'
application.config['MYSQL_DATABASE_DB'] = 'qa_course'
application.config['MYSQL_DATABASE_HOST'] = '52.2.195.57'
application.secret_key = 'FEF9B%399-!8EF6- 4B16-[9BD4-092B1<85D632D'
mysql.init_app(application)


class ServerError(Exception):
    pass


@application.errorhandler(404)
def page_not_found(e):
    # return render_template('index.html'), 404
    return render_template('WIP.html'), 404


@application.route("/index")
@application.route("/")
def index():
    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        username_session = username_session.split('@')[0]

        return render_template('index.html', session_user_name=username_session, row=session['rows'])
    return render_template('index.html')


@application.route("/cart")
def cart():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT product_id FROM cart WHERE user_id='{}';".format(session['user_id']))
    products_in_cart = cursor.fetchall()
    cart_list = []
    extended_cart = []
    quantities = []
    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        username_session = username_session.split('@')[0]
        if len(products_in_cart) > 0:
            for id in products_in_cart:
                cursor.execute("SELECT * FROM products WHERE product_id='{0}';".format(id[0]))
                cart_list.append(cursor.fetchone())
                cursor.execute("SELECT quantity FROM cart WHERE product_id='{0}' AND user_id='{1}';"
                               .format(id[0], session['user_id']))
                quantities.append(cursor.fetchone()[0])
            for i in range(len(cart_list)):
                extended_cart.append(list(cart_list[i]))
                extended_cart[i].append(quantities[i])
            return render_template('cart.html', session_user_name=username_session, row=session['rows'],
                                   cart=extended_cart, user_id=session['user_id'])
        else:
            return render_template('cart.html', session_user_name=username_session, row=session['rows'])
    return render_template('cart.html')


@application.route("/checkout")
def checkout():
    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        username_session = username_session.split('@')[0]

        return render_template('checkout.html', session_user_name=username_session)
    return render_template('checkout.html')


@application.route("/shop")
def shop():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products;")
    session["products"] = cursor.fetchall()
    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        username_session = username_session.split('@')[0]

        return render_template('shop.html', session_user_name=username_session, row=session['rows'],
                               products=session["products"], user_id=session['user_id'])
    return render_template('shop.html', products=session["products"])


@application.route("/single_product")
def single_product():
    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        username_session = username_session.split('@')[0]

        return render_template('single_product.html', session_user_name=username_session)
    return render_template('single_product.html')


@application.route('/action_login', methods=['POST'])
def action_login():
    conn = mysql.connect()
    cursor = conn.cursor()
    if 'username' in session:
        return redirect(url_for('index'))

    error = None
    try:
        if request.method == 'POST':
            email_form = escape(request.form['inputEmail'])
            cursor.execute("SELECT COUNT(1) FROM users WHERE email = '{0}';".format(email_form))

            if not cursor.fetchone()[0]:
                raise ServerError('Invalid username')

            password_form = request.form['inputPassword']
            cursor.execute("SELECT password FROM users WHERE email = '{0}';".format(email_form))

            for row in cursor.fetchall():
                hash_pwd = md5(md5(application.secret_key).hexdigest() + md5(password_form).hexdigest()).hexdigest()
                if hash_pwd == row[0]:
                    session['username'] = request.form['inputEmail']
                    cursor.execute("SELECT * FROM users WHERE email = '{0}';".format(email_form))
                    row = cursor.fetchone()
                    conn.close()
                    session['rows'] = row
                    session['user_id'] = row[0]
                    return redirect(url_for('index'))
            raise ServerError('Invalid password')
    except ServerError as e:
        error = str(e)
    conn.close()
    return render_template('index.html', error=error)


@application.route('/action_addproduct', methods=['POST'])
def action_addproduct():
    conn = mysql.connect()
    cursor = conn.cursor()
    if 'username' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        product_id = escape(request.form['productID'])
        user_id = escape(request.form['userID'])
        cursor.execute("SELECT COUNT(1) FROM cart WHERE product_id = '{0}' AND user_id = '{1}';".format(product_id,
                                                                                                        user_id))

        if cursor.fetchone()[0]:
            query = "UPDATE cart SET quantity = quantity + 1 WHERE user_id = {0} AND product_id = {1}".format(user_id,
                                                                                                              product_id)
            cursor.execute(query)
            conn.commit()
        else:
            query = "INSERT INTO cart (user_id, product_id, quantity) VALUES ('{0}', '{1}', {2})".format(user_id,
                                                                                                         product_id, 1)
            cursor.execute(query)
            conn.commit()
        # session['added_products'].append(product_id)
        conn.close()
        success = True
        return redirect(url_for('shop', submission_successful=success))
    conn.close()
    return render_template('index.html')


@application.route('/action_register', methods=['POST'])
def action_register():
    conn = mysql.connect()
    cursor = conn.cursor()
    # read the posted values from the UI
    _fname = request.form['inputFirstName']
    _lname = request.form['inputLastName']
    _email = escape(request.form['inputEmail'])
    _password = request.form['inputPassword']

    # validate the received values
    if not _email and not _password:
        return json.dumps({'html': '<span>Enter the required fields</span>'})
    else:
        json.dumps({'html': '<span>All fields good !!</span>'})

        cursor.execute("SELECT COUNT(1) FROM users WHERE email = '{0}';".format(_email))

        if cursor.fetchone()[0]:
            flash('Email already used')
            return redirect(url_for('index'))

        _hashed_password = md5(md5(application.secret_key).hexdigest() + md5(_password).hexdigest()).hexdigest()
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES ('{0}', '{1}', '{2}', '{3}')".format(
            _fname, _lname, _email, _hashed_password)
        cursor.execute(query)
        conn.commit()
        conn.close()
    conn.close()
    return redirect(url_for('index'))


@application.route('/action_logout')
def action_logout():
    session.pop('username', None)
    if "added_products" in session:
        session.pop("added_products", None)
    return redirect(url_for('index'))


@application.route('/action_remove_from_cart', methods=['POST'])
def action_remove_from_cart():
    conn = mysql.connect()
    cursor = conn.cursor()
    if 'username' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        product_id = escape(request.form['productID'])
        user_id = escape(request.form['userID'])
        query = "DELETE FROM cart WHERE user_id = {0} AND product_id = {1}".format(user_id, product_id)
        cursor.execute(query)
        conn.commit()

        conn.close()
        return redirect(url_for('cart'))

    conn.close()
    return redirect(url_for('cart'))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    application.run(host="0.0.0.0", port=port)
