import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from app.models.users import User

bp = Blueprint("auth", __name__)

@bp.route('/auth/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        hasError= False
        email = request.form['email'].strip()
        if len(email) == 0:
            hasError = True
            flash("Error: Enter Valid Email")
            return render_template('login.html')           
        password = request.form['password'].strip()
        if len(password) == 0:
            hasError = True
            flash("Error: Enter Valid Password")
            return render_template('login.html')
        
        #Check if email exists
        user = User.FromEmail(email)
        if user == None:
            #no email found
            hasError = True
            flash("Error: Login info did not match")
            return render_template('login.html')
        
        #Check password
        from werkzeug.security import check_password_hash
        if user.CheckPassword(password) == False:
            #entered wrong password
            hasError = True
            flash("Error: Login info did not match")
            return render_template('login.html')

        #Login Successful
        session['userid'] = user.id
        flash("Successfully logged in")
        return redirect(url_for('home'))
    
    return render_template('login.html')  # Placeholder for actual login implementation

@bp.route('/auth/logout')
def logout():   
    session.clear()
    flash("Successfully logged out")
    return redirect(url_for('home'))
    

@bp.route('/auth/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hasError= False

        name = request.form['name'].strip()
        if len(name) == 0:
            hasError = True
            flash("Error: Enter Valid Name")
        
        email = request.form['email'].strip()
        if len(email) == 0:
            hasError = True
            flash("Error: Enter Valid Email")
        
        password = request.form['password'].strip()
        if len(password) == 0:
            hasError = True
            flash("Error: Enter Valid Password")
        
        verifypassword = request.form['verifypassword'].strip()
        if len(verifypassword) == 0:
            hasError = True
            flash("Error: Confirm Password")

        if password != verifypassword:
            hasError = True
            flash("Error: Passwords do not match")

        #Check to see if email already registered
        check = User.FromEmail(email)
        if check != None:
            hasError = True
            flash("Error: Email already registered")

        #actually create user
        if not hasError:
            user = User.Create(name, email, password)
            flash("User registered successfully")
            return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('userid')

    if user_id == None:
        g.user = None 
    else:
        g.user = User.FromDB(user_id)

def permission_required(permission : str ):
    def decorator(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            if g.user == None:
                flash("Error: You must be logged in to access this page")
                return redirect(url_for('auth.login'))
            if g.user.HasPermission(permission):
                flash("Warning: You do not have permission to access that page")
                return redirect(url_for('auth.login'))
            return view(**kwargs)
        return wrapped_view
    return decorator