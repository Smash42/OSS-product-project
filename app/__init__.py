
import os
from flask import Flask, flash, g, redirect, render_template, request, session, url_for


from app.auth import permission_required
from app.models.product import ProductItem

def page_not_found(error):
    return render_template('page_not_found.html'), 404

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config =True)
    app.config.from_mapping(SECRET_KEY='dev')
    app.config.from_mapping(DATABASE=os.path.join(app.instance_path, 'products.sqlite'))

    try:
        #make folder if it doesn't exist
        os.makedirs(app.instance_path)
    except OSError:
        #just ignore error for now
        pass

    #Error Handlers
    app.register_error_handler(404, page_not_found)

    # Setup the database
    from . import db
    db.init_app(app)

    #Login Auth blueprint
    from . import auth
    app.register_blueprint(auth.bp)

    #Adds route to the app at /home
    @app.route('/')
    def home():

        return render_template('home.html')
    
    @app.route('/browse')
    def browse():
        products = ProductItem.GetAll()
        print(products)
        return render_template('browse.html', products=products)
        
    @app.route('/product/<int:product_id>')
    def product_detail(product_id):
        info = ProductItem.FromDB(product_id)
        if info is None:
            return render_template("page_not_found.html")  
        return render_template('product.html', product=info)
    
    @app.route('/product/add', methods=['GET', 'POST'])
    @permission_required('product.add')
    def add_product():
        if request.method == 'POST':
            hasError= False
            name = request.form['name'].strip()
            description = request.form['description'].strip()
            price = request.form['price'].strip()
            if (len(name) == 0 ):
                hasError = True
                flash("Error: Enter Valid Name")
            if len(description) == 0:
                hasError = True
                flash("Error: Enter Valid Description")

            if not hasError:
                product = ProductItem.Create(name, description, price)
                flash("Product created successfully")
                return redirect(url_for('product_detail', product_id=product.product_id))
            pass
         
        return render_template('add_product.html')
    
    @app.route('/product/<int:product_id>/edit', methods=['GET', 'POST'])
    @permission_required('product.edit')
    def edit_product(product_id):
        info = ProductItem.FromDB(product_id)
        if info is None:
            return render_template("page_not_found.html") 

        if request.method == 'POST':
            hasError= False
            name = request.form['name'].strip()
            description = request.form['description'].strip()
            price = request.form['price'].strip()
            hasError = False
            if not name:
                hasError = True
                flash("Error: Enter Valid Name")
            if not description:
                hasError = True
                flash("Error: Enter Valid Description")
            if not hasError:
                info.name = name
                info.description = description 
                info.price = price
                info.UpdateDatabase()
                flash("Product updated successfully")
                return redirect(url_for('product_detail', product_id=info.product_id)) 
            
        return render_template('edit_product.html', product = info)
    
    @app.route('/product/<int:product_id>/delete', methods=['GET', 'POST'])
    @permission_required('product.delete')
    def delete_product(product_id):
        info = ProductItem.FromDB(product_id)
        if info is None:
            return render_template("page_not_found.html")     
        if request.method == 'POST':
            info.Delete()
            flash("Product deleted successfully")
            return redirect(url_for('browse'))
            pass          
        return render_template('delete_product.html', product=info)
    
    @app.route('/cart')
    def cart():
        cart = session.get('cart', [])
        products = [ProductItem.FromDB(pid) for pid in cart]
        return render_template('cart.html')

    return app