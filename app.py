import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'cab_agency'
app.config["MONGO_URI"] = "mongodb+srv://root:rOOtUser@myfirstcluster.ilffs.mongodb.net/cab_agency?retryWrites=true&w=majority"

mongo = PyMongo(app)


@app.route('/')
@app.route('/get_cabs')
def get_cabs():
    return render_template('cabs.html', cabs=mongo.db.cabs.find())


# Add a cab
@app.route('/add_cab')
def add_cab():
    return render_template('addcab.html', types=mongo.db.types.find(),
                           brands=mongo.db.brands.find(),
                           models=mongo.db.models.find(),
                           bookings=mongo.db.bookings.find())


# Insert a Cab
@app.route('/insert_cab', methods=['POST'])
def insert_cab():
    cabs = mongo.db.cabs
    # get the form and convert to a dictionary
    cabs.insert_one(request.form.to_dict())
    # get the form fields with data in them
    return redirect(url_for('get_cabs'))


# Edit a Cab selection
# pre-populated based on the information returned in the task.
@app.route('/edit_cab/<cab_id>')
def edit_cab(cab_id):
    a_cab = mongo.db.cabs.find_one({"_id": ObjectId(cab_id)})
    # prepolulated based on the collection
    # returned in the types, brands and models cursor
    all_types = mongo.db.types.find()
    all_brands = mongo.db.brands.find()
    all_models = mongo.db.models.find()
    return render_template('editcab.html', cab=a_cab,
                           types=all_types, brands=all_brands,
                           models=all_models)


# update Cab entry
@app.route('/update_cab/<cab_id>', methods=['POST'])
def update_cab(cab_id):
    # access the database collection
    cabs = mongo.db.cabs
    # call the update function, specify an id
    cabs.update({'_id': ObjectId(cab_id)},
    {
        'vehicle_type': request.form.get('vehicle_type'),
        'brand_name': request.form.get('brand_name'),
        'model_name': request.form.get('model_name'),
        'cab_location': request.form.get('cab_location'),
        'email': request.form.get('email'),
        'tel_nr': request.form.get('tel_nr'),
        'cab_picture': request.form.get('cab_picture')
    })
    return redirect(url_for('get_cabs'))
    # specify the form fields to match the keys on the task collection


# delete a Cab entry
@app.route('/delete_cab/<cab_id>')
def delete_cab(cab_id):
    mongo.db.cabs.remove({'_id': ObjectId(cab_id)})
    return redirect(url_for('get_cabs'))


# find a book by using a search field
@app.route('/get_one/<cab_id>', methods=['GET'])
def get_one(cab_id):
    cab = mongo.db.cabs
    cab = mongo.db.cabs.find_one({'_id': ObjectId(cab_id)})
    return render_template('findcab.html', cab=cab)


# get booked cabs
@app.route('/get_bookings')
def get_bookings():
    return render_template('bookings.html',
                           bookings=mongo.db.bookings.find())


# add booking
@app.route('/add_booking')
def add_booking():
    return render_template('addbooking.html', types=mongo.db.types.find(),
                           brands=mongo.db.brands.find(),
                           models=mongo.db.models.find(),
                           bookings=mongo.db.bookings.find())


# Book a Cab
@app.route('/insert_booking', methods=['POST'])
def insert_booking():
    bookings = mongo.db.bookings
    # get the form and convert to a dictionary
    bookings.insert_one(request.form.to_dict())
    return redirect(url_for('get_bookings'))


# <---- Manage vehicle Types, Brands & Models ---->

# Gets the vehicle Types
@app.route('/get_types')
def get_types():
    return render_template('types.html',
                           types=mongo.db.types.find())


# edits a vehicle Type
@app.route('/edit_type/<type_id>')
def edit_type(type_id):
    return render_template('edittype.html',
                           type=mongo.db.types.find_one(
                            {'_id': ObjectId(type_id)}))


# updates vehicle Type
@app.route('/update_type/<type_id>', methods=['POST'])
def update_type(type_id):
    mongo.db.types.update(
        {'_id': ObjectId(type_id)},
        {'vehicle_type': request.form.get('vehicle_type')})
    return redirect(url_for('get_types'))
# ------ End of Vehicle Type----------

# ------ Vehicle Brand----------


"""
# Insert a Cab
@app.route('/insert_brand', methods=['POST'])
def insert_brand():
    brands = mongo.db.brands
    # get the form and convert to a dictionary
    brands.insert_one(request.form.to_dict())
    # get the form fields with data in them
    return redirect(url_for('get_brand'))
"""


# Gets the Brand Name
@app.route('/get_brand')
def get_brand():
    return render_template('brands.html',
                           brands=mongo.db.brands.find())


# edits a Brand Name
@app.route('/edit_brand/<brand_id>')
def edit_brand(brand_id):
    return render_template('brands.html',
                           brand=mongo.db.brands.find_one(
                            {'_id': ObjectId(brand_id)}))


# updates Brand
@app.route('/update_brand/<brand_id>', methods=['POST'])
def update_brand(brand_id):
    mongo.db.brands.update(
        {'_id': ObjectId(brand_id)},
        {'brand_name': request.form.get('brand_name')})
    return redirect(url_for('get_brand'))

# ------ End of Vehicle Brand----------


# ------ Vehicle Model----------

# Get the Model
@app.route('/get_model')
def get_model():
    return render_template('models.html',
                           models=mongo.db.models.find())


# edit the Model
@app.route('/edit_model/<model_id>')
def edit_model(model_id):
    return render_template('models.html',
                           model=mongo.db.models.find_one(
                            {'_id': ObjectId(model_id)}))


# updates Model
@app.route('/update_model/<model_id>', methods=['POST'])
def update_model(model_id):
    mongo.db.models.update(
        {'_id': ObjectId(model_id)},
        {'model_name': request.form.get('model_name')})
    return redirect(url_for('get_model'))

# ------ End of Vehicle Brand----------


# ------ Delete functions--------

#  delete Types
@app.route('/delete_type/<type_id>')
def delete_type(type_id):
    mongo.db.types.remove({'_id': ObjectId(type_id)})
    return redirect(url_for('get_types'))


#  delete Brands
@app.route('/delete_brand/<brand_id>')
def delete_brand(brand_id):
    mongo.db.brands.remove({'_id': ObjectId(brand_id)})
    return redirect(url_for('get_brand'))


#  delete Models
@app.route('/delete_model/<model_id>')
def delete_model(model_id):
    mongo.db.models.remove({'_id': ObjectId(model_id)})
    return redirect(url_for('get_model'))

# ------ End Delete---------


# add Types
@app.route('/insert_type', methods=['POST'])
def insert_type():
    types = mongo.db.types
    types_doc = {'vehicle_type': request.form.get('vehicle_type')}
    types.insert_one(types_doc)
    return redirect(url_for('get_types'))


# render a view and add a new type
@app.route('/new_type')
def new_type():
    return render_template('addtype.html')


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
                debug=True)