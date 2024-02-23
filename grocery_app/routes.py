from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from flask_bcrypt import Bcrypt
from flask_login import login_user, logout_user, login_required, current_user
from grocery_app.models import GroceryStore, GroceryItem, User
from grocery_app.forms import GroceryStoreForm, GroceryItemForm, SignUpForm, LoginForm

# Import app and db from events_app package so that we can run app
from grocery_app.extensions import app, db

main = Blueprint("main", __name__)
bcrypt = Bcrypt(app)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    """Home page"""
    all_stores = GroceryStore.query.all()
    print(all_stores)
    return render_template('home.html', all_stores=all_stores)

# ----------------------
# New Store Route
@login_required
@main.route('/new_store', methods=['GET', 'POST'])
def new_store():
    """Create a new store"""
    # Create a GroceryStoreForm
    form = GroceryStoreForm()
    # If form was submitted and was valid:
    if form.validate_on_submit():
        # - create a new GroceryStore object and save it to the database,
        new_grocery_store = GroceryStore(
            title = form.title.data,
            address = form.address.data,
            created_by = current_user.username,
        )

        db.session.add(new_grocery_store)
        db.session.commit()
        # - flash a success message, and
        flash('Store was created successfully')
        # - redirect the user to the store detail page.
        return redirect(url_for('main.store_detail', store_id=new_grocery_store.id))

    # Send the form to the template and use it to render the form fields
    return render_template('new_store.html', form=form)

# ----------------------
# Item Detail Route
@login_required
@main.route('/new_item', methods=['GET', 'POST'])
def new_item():
    """Create new item"""
    # Create a GroceryItemForm
    form = GroceryItemForm()
    # If form was submitted and was valid:
    if form.validate_on_submit():
        # - create a new GroceryItem object and save it to the database,
        new_grocery_item = GroceryItem(
            name = form.name.data,
            price = form.price.data,
            category = form.category.data,
            photo_url = form.photo_url.data,
            created_by = current_user.username,
        )

        db.session.add(new_grocery_item)
        db.session.commit()
        # - flash a success message, and
        flash('New item was created successfully.')
        # - redirect the user to the item detail page.
        return redirect(url_for('main.item_detail', item_id=new_grocery_item.id))
    # Send the form to the template and use it to render the form fields
    return render_template('new_item.html', form=form)

# ----------------------
# Store Detail Route
@login_required
@main.route('/store/<store_id>', methods=['GET', 'POST'])
def store_detail(store_id):
    """Store Details"""
    store = GroceryStore.query.get(store_id)
    # Create a GroceryStoreForm and pass in `obj=store`
    form = GroceryStoreForm(obj=store)
    # If form was submitted and was valid:
    if form.validate_on_submit():
        # - update the GroceryStore object and save it to the database,
        form.populate_obj(store)

        db.session.commit()
        # - flash a success message, and
        flash('Store was updated successfully.')
        # - redirect the user to the store detail page.
        return redirect(url_for('main.store_details', store_id=store.id))
    # Send the form to the template and use it to render the form fields
    store = GroceryStore.query.get(store_id)
    return render_template('store_detail.html', store=store, form=form)

# ----------------------
# Item Detail Route
@login_required
@main.route('/item/<item_id>', methods=['GET', 'POST'])
def item_detail(item_id):
    """Item Details"""
    item = GroceryItem.query.get(item_id)
    # Create a GroceryItemForm and pass in `obj=item`
    form = GroceryItemForm(obj=item)
    # If form was submitted and was valid:
    if form.validate_on_submit():
        # - update the GroceryItem object and save it to the database,
        form.populate_obj(item)

        db.commit()
        # - flash a success message, and
        flash('Item was updated successfully.')
        # - redirect the user to the item detail page.
        return redirect(url_for('main.item_detail', store_id=item.id))
    # Send the form to the template and use it to render the form fields
    item = GroceryItem.query.get(item_id)
    return render_template('item_detail.html', item=item)

# -----------------------------------
# Add item
@main.route('/add_to_shopping_list/<item_id>', methods=['POST'])
def add_to_shopping_list(item_id):
    """adds item to current_user's shopping list"""
    item = GroceryItem.query.get(item_id)

    if item not in current_user.items:
        current_user.items.append(item)
        db.session.commit()
        flash("Item added succesfully")

    flash('Item was not added. Try again')
    return redirect(url_for('main.item)detail', item_id=item_id))

# --------------------------
# See all items
@main.route('/shopping_list')
@login_required
def shopping_list():
    """ get logged in user's shopping list items and display shopping list items in a template """
    user = current_user
    items = user.items

    return render_template('shopping_list.html', items=items)

auth = Blueprint("auth", __name__)

# ---------------------
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    """Signup"""
    print('in signup')
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Account Created.')
        print('created')
        return redirect(url_for('auth.login'))
    print(form.errors)
    return render_template('signup.html', form=form)

# ---------------------
@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Login"""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, remember=True)
        next_page = request.args.get('next')
        return redirect(next_page if next_page else url_for('main.homepage'))
    return render_template('login.html', form=form)

# ---------------------
@auth.route('/logout')
@login_required
def logout():
    """Logout"""
    logout_user()
    return redirect(url_for('main.homepage'))
