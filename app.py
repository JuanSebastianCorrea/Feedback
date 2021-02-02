from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegisterUserForm, LoginUserForm, FeedbackForm
# from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///feedback_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)


toolbar = DebugToolbarExtension(app)


@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/register', methods=["GET", "POST"])
def register_user():
    form = RegisterUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username=username, pwd=password, email=email, first_name=first_name, last_name=last_name)
        
        db.session.add(user)
        db.session.commit()
        session["username"] = user.username
        flash('Welcome! Successfully created your account!')
        return redirect(f'/users/{user.username}')

    return render_template('register.html', form=form)



@app.route('/login', methods=["GET", "POST"])
def login_user():

    if "username" in session:
        return redirect(f'/users/{session["username"]}')

    form = LoginUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username=username, pwd=password)
        if user:
            session["username"] = user.username
            flash(f"Welcome back, {user.username}!")
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ["Invalid username/password"]
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_user():
    session.pop("username")
    flash("Goodbye!")
    return redirect('/')

@app.route('/users/<username>')
def show_user_info(username):
    if "username" not in session and session["username"] != username:
        flash("Please login first!")
        return redirect('/login')
    
    user = User.query.get_or_404(username)
    return render_template('feedback.html', user=user)

# @app.route('/users/<username>/delete')
# def delete_user(username):

#     user = User.query.get_or_404(username)


@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def add_feedback(username):
    if "username" not in session:
        flash("Please login first!")
        return redirect('/login')
    elif username != session["username"]:
        flash("You are not authorized to post for someone else!")
        return redirect(f'/users/{username}')
    
    else:
        form = FeedbackForm()

        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            
            feedback = Feedback(title=title, content=content, username=username)
            db.session.add(feedback)
            db.session.commit()
            return redirect(f'/users/{username}')


        return render_template('add_feedback.html', form=form)

@app.route('/feedback/<int:feedbackid>/update', methods=["GET", "POST"])
def update_feedback(feedbackid):

    feedback = Feedback.query.get_or_404(feedbackid)
    
    if "username" not in session:
        flash("Please login first!")
        return redirect('/login')
    elif feedback.username != session["username"]:
        flash("You are not authorized to update someone else's feedback!")
        return redirect(f'/users/{session["username"]}')
    
    else:
        form = FeedbackForm(obj=feedback)

        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data
            
            db.session.commit()
            return redirect(f'/users/{feedback.username}')


        return render_template('update_feedback.html', form=form, feedback=feedback)

@app.route('/feedback/<int:feedbackid>/delete')
def delete_feedback(feedbackid):

    feedback = Feedback.query.get_or_404(feedbackid)

    if "username" not in session:
        flash("Please login first!")
        return redirect('/login')
    elif feedback.username != session["username"]:
        flash("You are not authorized to delete someone else's feedback!")
        return redirect(f'/users/{session["username"]}')
    
    else:
        db.session.delete(feedback)
        db.session.commit()
        return redirect(f'/users/{session["username"]}')