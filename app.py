from flask import Flask, render_template, flash, request, url_for, redirect, session
from dbconnect import connection
from wtforms import Form, BooleanField, TextField, PasswordField, StringField, validators, RadioField, FloatField, IntegerField, TextAreaField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from passlib.hash import sha256_crypt
from functools import wraps
from flask_wtf import FlaskForm
import re
from flask_mysqldb import MySQL
import MySQLdb.cursors



app = Flask(__name__)

def connection():
    conn = MySQLdb.connect(
        Host = "localhost",
        User = "root",
        Password = "",
        Database = "dentalbusiness"
        Cursor = "dictCursor"
        
    )
    cur = conn.cursor()
    return cur, conn

app.secret_key = 'key123'

# Upload Image---------------------------------------------------------------------------------------------------------------------###
images = UploadSet('images', IMAGES)
configure_uploads(app, images) 

# Home Page------------------------------------------------------------------------------------------------------------------------###
@app.route('/')
def homepage():
    return render_template("home.html")

# Dashboard------------------------------------------------------------------------------------------------------------------------###
@app.route('/dashboard/')
def dashboard():
    return redirect(url_for("dashboard"))

# About----------------------------------------------------------------------------------------------------------------------------###
@app.route('/about/')
def about():
    return render_template("about.html")

@app.route('/addcart', methods=['POST'])
def AddCart():
    try:
        pass
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

# Checkout-------------------------------------------------------------------------------------------------------------------------###
@app.route('/checkout/')
def checkout():
    if 'Shoppingcart'not in session or len(session['Shoppingcart'])<=0:
        cur, conn = connection()
        if request.method == "GET":
            if (cur.execute("SELECT * FROM users WHERE role_id = ('1')")):

                return redirect(url_for("clinic"))
            elif (cur.execute("SELECT * FROM users WHERE role_id = ('2')")):
                return redirect(url_for("lab"))
            elif (cur.execute("SELECT * FROM users WHERE role_id = ('3')")):
                return redirect(url_for("manufacturer"))

    subtotal = 0
    grandtotal = 0
    for key, product in session['Shoppingcart'].items():
        discount = (product['discount']/100) * float(product['price'])
        subtotal += float(product['price']) * int(product['quantity'])
        subtotal -= discount
        tax = ("%0.2f" % (.06 * float(subtotal)))
        grandtotal = float("%0.2f" % (1.06 * subtotal))

    
    return render_template("checkout.html", grandtotal = grandtotal)

# Payment Successful---------------------------------------------------------------------------------------------------------------###
@app.route('/payment_successful/')
def payment_successful():
    if 'Shoppingcart'not in session or len(session['Shoppingcart'])<=0:
        cur, conn = connection()
        if request.method == "GET":
            if (cur.execute("SELECT * FROM users WHERE role_id = ('1')")):

                return redirect(url_for("clinic"))
            elif (cur.execute("SELECT * FROM users WHERE role_id = ('2')")):
                return redirect(url_for("lab"))
            elif (cur.execute("SELECT * FROM users WHERE role_id = ('3')")):
                return redirect(url_for("manufacturer"))

    subtotal = 0
    grandtotal = 0
    for key, product in session['Shoppingcart'].items():
        discount = (product['discount']/100) * float(product['price'])
        subtotal += float(product['price']) * int(product['quantity'])
        subtotal -= discount
        tax = ("%0.2f" % (.06 * float(subtotal)))
        grandtotal = float("%0.2f" % (1.06 * subtotal))

    
    return render_template("payment_successful.html", grandtotal = grandtotal)

# Add to Cart---------------------------------------------------------------------------------------------------------------------###
@app.route('/addcart', methods=['POST'])
def AddCart():
    try:
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity'))
        cur, conn = connection()
        data = cur.execute("SELECT * FROM labProducts WHERE id= %s",product_id)
        products1 = cur.fetchone()
        if request.method == "POST":
            DictItems = {product_id:{'name':products1[1], 'price':products1[3], 'discount': products1[4], 'quantity':quantity}}
            print(product_id, quantity)
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    print('This  product is already addded in your cart')
                    for key, item in session['Shoppingcart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            item['quantity'] = item['quantity'] + 1
                else:
                    session['Shoppingcart'] = MagerDicts(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)

    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

# Lab: Add to cart---------------------------------------------------------------------------------------------------------------------###
@app.route('/addcart_lab', methods=['POST'])
def AddCart_lab():
    try:
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity'))
        cur, conn = connection()
        data = cur.execute("SELECT * FROM manufacturerProduct WHERE id= %s",product_id)
        products1 = cur.fetchone()
        if request.method == "POST":
            DictItems = {product_id:{'name':products1[1], 'price':products1[3], 'discount': products1[4], 'quantity':quantity}}
            print(product_id, quantity)
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    print('This  product is already addded in your cart')
                    for key, item in session['Shoppingcart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            item['quantity'] = item['quantity'] + 1
                else:
                    session['Shoppingcart'] = MagerDicts(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)

    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

# Show cart with tax and total---------------------------------------------------------------------------------------------------------------------###
@app.route('/carts', methods=['GET'])
def getCart():
    if 'Shoppingcart'not in session or len(session['Shoppingcart'])<=0:
        cur, conn = connection()
        if request.method == "GET":
            if (cur.execute("SELECT * FROM users WHERE role_id = ('1')")):

                return redirect(url_for("clinic"))
            elif (cur.execute("SELECT * FROM users WHERE role_id = ('2')")):
                return redirect(url_for("lab"))
            elif (cur.execute("SELECT * FROM users WHERE role_id = ('3')")):
                return redirect(url_for("manufacturer"))

    subtotal = 0
    grandtotal = 0
    for key, product in session['Shoppingcart'].items():
        discount = (product['discount']/100) * float(product['price'])
        subtotal += float(product['price']) * int(product['quantity'])
        subtotal -= discount
        tax = ("%0.2f" % (.06 * float(subtotal)))
        grandtotal = float("%0.2f" % (1.06 * subtotal))

    return render_template('products/carts.html', tax=tax, grandtotal=grandtotal)


# Update in cart---------------------------------------------------------------------------------------------------------------------###
@app.route('/updatecart/<int:code>', methods=['POST'])
def updatecart(code):
    if 'Shoppingcart'not in session or len(session['Shoppingcart']) <= 0:
        return redirect('carts')

    if request.method == "POST":
        quantity = request.form.get('quantity')
        try:
            session.modified = True
            for key, item in session['Shoppingcart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    flash('Item is updated')
                    return redirect(url_for('getCart'))
        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))

# Delete item from cart---------------------------------------------------------------------------------------------------------------------###
@app.route('/deleteitem/<int:id>', methods=['GET'])
def deleteitem(id):
    if 'Shoppingcart'not in session or len(session['Shoppingcart']) <= 0:
        return redirect('carts')
    try:
        session.modified = True
        for key, item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                return redirect(url_for('getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))

# Clear cart-------------------------------------------------------------------------------------------------------------------------------###
@app.route('/clearcart')
def clearcart():
    try:
        session.pop('Shoppingcart', None)
        return redirect('carts')
    except Exception as e:
        print(e)

# Clinic homepage---------------------------------------------------------------------------------------------------------------------###
@app.route('/clinic/')
def clinic():
    page = request.args.get('page',1, type=int)
    #per_page = 4
    cur, conn = connection()
    data = cur.execute("SELECT * FROM labProducts where stock>0 order by name, price DESC LIMIT 10 offset 0")
    products1 = cur.fetchall()
    return render_template("clinic.html", products=products1) 

# single product details from lab products---------------------------------------------------------------------------------------------------------------------###
@app.route('/products/<int:id>')
def single_product_detail(id):
    cur, conn = connection()
    data = cur.execute("SELECT * FROM labProducts WHERE id= %s", (id,))
    products1 = cur.fetchall()
    return render_template('products/single_product_detail.html', products=products1)

# single product details from manufacturer products---------------------------------------------------------------------------------------------------------------------###
@app.route('/products/<string:id>')
def single_product_detail_Manuf(id):
    cur, conn = connection()
    data = cur.execute("SELECT * FROM manufacturerProduct WHERE id= %s", (id,))
    products1 = cur.fetchall()
    return render_template('products/single_product_detail_Manuf.html', products=products1)

# Lab homepage--------------------------------------------------------------------------------------------------------------------------------------------------###
@app.route('/lab/')
def lab():
    cur, conn = connection()
    data = cur.execute("SELECT * FROM manufacturerProduct order by name, price DESC")
    products1 = cur.fetchall()
    return render_template("lab.html", products=products1)

# Lab products---------------------------------------------------------------------------------------------------------------------------------------------------###
@app.route('/labproduct/')
def labproduct():
    cur, conn = connection()
    data = cur.execute("SELECT * FROM labProducts order by name, price DESC")
    products1 = cur.fetchall()
    return render_template("products/labproduct.html", products=products1)

# Lab: Add products form---------------------------------------------------------------------------------------------------------------------###
class Addproducts_lab(Form):
    name = StringField('Name', [validators.DataRequired()])
    username = StringField('Seller', [validators.DataRequired()])
    price = StringField('Price', [validators.DataRequired()])
    discount = StringField('Discount', default=0)
    stock = StringField('Stock', [validators.DataRequired()])
    discription = StringField('Discription', [validators.DataRequired()])

# Add products in to the lab---------------------------------------------------------------------------------------------------------------------###
@app.route('/addproduct_lab/', methods=['GET','POST'])
def addproduct_lab():
    try:
        form = Addproducts_lab(request.form)

        if request.method=="POST" and form.validate():
            name = form.name.data
            username = form.username.data
            price = form.price.data
            discount = form.discount.data
            stock = form.stock.data
            description = form.description.data
            cur, conn = connection()

            cur.execute("INSERT INTO labProducts (name, username, price, discount, stock, description) VALUES (%s, %s, %s, %s, %s, %s)",
                        (name, username, price, discount, stock, description))
            conn.commit()
            flash(f'The product {name} was added in database','success')
            cur.close()
            conn.close()

            return redirect(url_for('lab'))
        return render_template('products/addproduct_lab.html', form=form, title='Add a Product')
    except Exception as e:
        return(str(e))

# Update product in the lab---------------------------------------------------------------------------------------------------------------------###
@app.route('/updateproduct_lab/<int:id>', methods=['GET','POST'])
def updateproduct_lab(id):
    try:
        form = Addproducts_lab(request.form)
        record = None

        if request.method=="POST" and form.validate():
            cur, conn = connection()

            cur.execute("UPDATE manufacturerProduct SET (name, username, price, discount, stock, description) WHERE id = %s VALUES (%s, %s, %s, %s, %s, %s)",
                id,
                form.name.data,
                form.username.data,
                form.price.data,
                form.discount.data,
                form.stock.data,
                form.description.data,
                )

            record = c.fetchone()
            print(record)
            conn.commit()
            flash(f'The product {name} was updated in database','success')
            cur.close()
            conn.close()
            return redirect(url_for('manufacturer'))

        return render_template('products/updateproduct_lab.html',  form=form, product = record, title='Update a Product')
    except Exception as e:
        return(str(e))

# delete product from lab---------------------------------------------------------------------------------------------------------------------###
@app.route('/deleteproduct_lab/<string:id>', methods=['POST'])
def deleteproduct_lab(id):
    try:
        
        product = Addproducts_lab(request.form)
        if request.method=="POST":
            name = product.name.data 
            cur, conn = connection()
            print("Displaying Manufacturer products Before Deleting it")
            cur.execute("DELETE FROM labProducts WHERE id= %s",id)
            record = c.fetchone()
            print(record)
            conn.commit()
            flash(f'The product {name} was deleted from your record','success')
            cur.close()
            conn.close()
            return redirect(url_for('lab'))
    except Exception as e:
        return(str(e))

# manufacturer homepage---------------------------------------------------------------------------------------------------------------------###
@app.route('/manufacturer/')
def manufacturer():
    cur, conn = connection()
    data = cur.execute("SELECT * FROM manufacturerProduct order by name, price DESC")
    products1 = cur.fetchall()
    return render_template("manufacturer.html", products=products1)

# Manufacturer: Add product form---------------------------------------------------------------------------------------------------------------------###
class Addproducts(Form):
    name = StringField('Name', [validators.DataRequired()])
    username = StringField('Seller', [validators.DataRequired()])
    """ image = FileField('Image', validators=[FileRequired(), FileAllowed(images, 'Images only!')]) """
    price = StringField('Price', [validators.DataRequired()])
    discount = StringField('Discount', default=0)
    stock = StringField('Stock', [validators.DataRequired()])
    discription = StringField('Discription', [validators.DataRequired()])

# Add product in the manufacturer---------------------------------------------------------------------------------------------------------------------###
@app.route('/addproduct/', methods=['GET','POST'])
def addproduct():
    try:
        form = Addproducts(request.form)

        if request.method=="POST" and form.validate():
            name = form.name.data
            username = form.username.data
            """ image = url """
            price = form.price.data
            discount = form.discount.data
            stock = form.stock.data
            description = form.description.data
            cur, conn = connection()

            cur.execute("INSERT INTO manufacturerProduct (name, username, price, discount, stock, description) VALUES (%s, %s, %s, %s, %s, %s)",
                        (name, username, price, discount, stock, description))
            conn.commit()
            flash(f'The product {name} was added in database','success')
            cur.close()
            conn.close()

            return redirect(url_for('manufacturer'))
        return render_template('products/addproduct.html', form=form, title='Add a Product')
    except Exception as e:
        return(str(e))

# Update product in the manufacturer---------------------------------------------------------------------------------------------------------------------###
@app.route('/updateproduct/<string:id>', methods=['GET','POST'])
def updateproduct(id):
    try:
        form = Addproducts(request.form)
        record = None

        if request.method=="POST" and form.validate():
            cur, conn = connection()

            cur.execute("UPDATE manufacturerProduct SET (name, username, price, discount, stock, description) WHERE id = %s VALUES (%s, %s, %s, %s, %s, %s)",
                id,
                form.name.data,
                form.username.data,
                form.price.data,
                form.discount.data,
                form.stock.data,
                form.description.data,
                )

            record = cur.fetchone()
            print(record)
            conn.commit()
            flash(f'The product {name} was updated in database','success')
            cur.close()
            conn.close()
            return redirect(url_for('manufacturer'))

        return render_template('products/updateproduct.html',  form=form, product = record, title='Update a Product')
    except Exception as e:
        return(str(e))

# Delete product from manufacturer---------------------------------------------------------------------------------------------------------------------###
@app.route('/delete_product/<int:id>')
def delete_product(id):
    # create cursor
    print("step1")
    cur,conn = connection()

    #execute
    cur.execute("DELETE FROM manufacturerProduct WHERE id = %s", id)
    print("step2")

    #Commit to DB
    conn.commit()

    #close connection
    cur.close()
    conn.close

    flash('Product Deleted', 'success')
    return redirect(url_for('dashboard'))

# exception handler-------------------------------------------------------------------------------------------------------------------###
@app.errorhandler(error)
def page_not_found(e):
    return render_template("error.html")

# Login required---------------------------------------------------------------------------------------------------------------------###
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login_page'))
    return wrap

# Logout---------------------------------------------------------------------------------------------------------------------###
@app.route("/logout/")
@login_required
def logout():
    session.clear()
    flash("You have been logged out!")
    gc.collect()
    return redirect(url_for("homepage"))

# Login---------------------------------------------------------------------------------------------------------------------###
@app.route('/login/', methods=["GET","POST"])
def login_page():
    error = ''
    cur, conn = connection()
    if request.method == "POST":
        username = request.form['username']
        if (cur.execute("SELECT * FROM users WHERE username = %s AND role_id = ('1')", [username])):
            data = cur.fetchone()[1] #defines the value of Coloumn 1 in the table
            if sha256_crypt.verify(request.form['password'], data):
                session['logged_in'] = True
                session['username'] = request.form['username']
                flash("You are now logged in")
                return redirect(url_for("clinic"))
            else:
                flash('Invalid Username or Password...!!', 'danger')
        if (cur.execute("SELECT * FROM users WHERE username = %s AND role_id = ('2')", [username])):
            data = cur.fetchone()[1]
            if sha256_crypt.verify(request.form['password'], data):
                session['logged_in'] = True
                session['username'] = request.form['username']
                flash("You are now logged in")
                return redirect(url_for("lab"))
            else:
                flash('Invalid Username or Password...!!', 'danger')
        if (cur.execute("SELECT * FROM users WHERE username = %s AND role_id = ('3')", [username])):
            data = cur.fetchone()[1]
            if sha256_crypt.verify(request.form['password'], data):
                session['logged_in'] = True
                session['username'] = request.form['username']
                flash("You are now logged in")
                return redirect(url_for("manufacturer"))
            else:
                flash('Invalid Username or Password...!!', 'danger')
        else:
            error = "Invalid credentials, try again."

    return render_template("login.html", error=error)


# registeration form---------------------------------------------------------------------------------------------------------------------###
class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [ 
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password')
    role_id=RadioField('Type of User',choices=[('1','Dental Clinic'),('2','Dental Lab'),('3','Manufacturer')])
    accept = BooleanField('I accept the Terms of Service and Privacy Notice', [validators.DataRequired()])

# register---------------------------------------------------------------------------------------------------------------------###
@app.route('/register/', methods=["GET","POST"])
def register_page():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))
        role_id = form.role_id.data
        cur, conn = connection()
        cur.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cur.fetchone()

        # If account exists show error and validation checks
        if user:
            flash('Account already exists!', 'danger')
            return redirect(url_for('login_page'))
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!', 'danger')
            return redirect(url_for('register'))
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash('Username must contain only characters and numbers!', 'danger')
            return redirect(url_for('register'))
        elif not username or not password or not email:
            flash('Please fill all the fields', 'danger')
            return redirect(url_for('register'))
        else:
            # Execute query
            cur.execute("INSERT INTO users(username, email, password, role_id) VALUES(%s, %s, %s, %s)", (username, email, password, role_id))
            conn.commit()
            flash(f'Welcome {form.username.data} '"Thanks for registering!",'success')
            cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login_page'))
    return render_template('register.html', form=form) 

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=8080)