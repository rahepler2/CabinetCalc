from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('cabinets.db')
    conn.row_factory = sqlite3.Row
    return conn

class Customer:
    def __init__(self, customer_id, name, email):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.jobs = []

    def add_job(self, job):
        self.jobs.append(job)


class Cabinet:
    def __init__(self, conn, collection, location, width, carcass_interior, drawer_wood, hinge_style, ceiling_height, num_drawers, num_doors, frame_wood, glass, back_panel, toe_kick, end_panel, finish):
        self.conn = conn
        self.collection = collection
        self.location = location
        self.width = width
        self.carcass_interior = carcass_interior
        self.drawer_wood = drawer_wood
        self.hinge_style = hinge_style
        self.ceiling_height = ceiling_height
        self.num_drawers = num_drawers
        self.num_doors = num_doors
        self.frame_wood = frame_wood
        self.glass = glass
        self.back_panel = back_panel
        self.toe_kick = toe_kick
        self.end_panel = end_panel
        self.finish = finish
        self.load_pricing()

    def load_pricing(self):
        self.collection_cost_value = self.get_collection_cost()
        self.location_cost_value = self.get_location_cost()
        self.width_cost_value = self.get_width_factor()
        self.carcass_cost_value = self.get_carcass_interior_cost()
        self.drawer_wood_cost_value = self.get_drawer_wood_cost()
        self.hinge_style_cost = self.get_hinge_style_cost()
        self.ceiling_height_cost = self.get_ceiling_height_cost()
        self.num_drawers_cost_value = self.get_num_drawers_cost()
        self.num_doors_cost_value = self.get_num_doors_cost()
        self.frame_wood_cost_value = self.get_frame_wood_cost()
        self.glass_cost_value = self.get_glass_cost()
        self.back_panel_cost_value = self.get_back_panel_cost()
        self.toe_kick_cost_value = self.get_toe_kick_cost()
        self.end_panel_cost_value = self.get_end_panel_cost()
        self.finish_cost_value = self.get_finish_cost()

    def get_collection_cost(self):
        cur = self.conn.cursor()
        cur.execute("SELECT price_multiplier FROM collections WHERE name=?", (self.collection,))
        row = cur.fetchone()
        return row[0] if row else 0

    def get_location_cost(self):
        cur = self.conn.cursor()
        cur.execute("SELECT price FROM locations WHERE name=?", (self.location,))
        row = cur.fetchone()
        return row[0] if row else 0

    def total_collection_cost(self):
        return self.get_location_cost() * self.get_collection_cost()

    def get_width_factor(self):
        cur = self.conn.cursor()
        cur.execute("SELECT factor FROM widths WHERE width=?", (self.width,))
        row = cur.fetchone()
        factor = row[0] if row else 0
        if self.location in ["R Front", "Refrigerator", "DW Front"]:
            factor *= 0.5
        return factor

    def get_carcass_interior_cost(self):
        cur = self.conn.cursor()
        cur.execute("SELECT price FROM carcass_materials WHERE name=?", (self.carcass_interior,))
        row = cur.fetchone()
        return row[0] if row else 0

    def get_drawer_wood_cost(self):
        if self.num_drawers == 0:
            return 0
        cur = self.conn.cursor()
        cur.execute("SELECT price FROM drawer_woods WHERE name=?", (self.drawer_wood,))
        row = cur.fetchone()
        drawer_price = row[0] if row else 0
        base_cost = (((self.width * 2) + 44) * 8 / 144) * self.num_drawers
        return base_cost * drawer_price

    def get_hinge_style_cost(self):
        cur = self.conn.cursor()
        cur.execute("SELECT price_multiplier FROM hinge_styles WHERE name=?", (self.hinge_style,))
        row = cur.fetchone()
        return row[0] if row else 1

    def get_ceiling_height_cost(self):
        cur = self.conn.cursor()
        cur.execute("SELECT price_multiplier FROM ceiling_heights WHERE height=?", (self.ceiling_height,))
        row = cur.fetchone()
        return row[0] if row else 1

    def get_num_drawers_cost(self):
        return self.num_drawers * 100

    def get_num_doors_cost(self):
        return self.num_doors * 50

    def get_frame_wood_cost(self):
        cur = self.conn.cursor()
        cur.execute("SELECT price FROM frame_woods WHERE name=?", (self.frame_wood,))
        row = cur.fetchone()
        return self.width * 36 / 144 * row[0] if row else 0

    def get_glass_cost(self):
        return self.num_doors * 300 if self.glass == "Yes" else 0

    def get_back_panel_cost(self):
        cur = self.conn.cursor()
        cur.execute("SELECT price_multiplier FROM back_panels WHERE name=?", (self.back_panel,))
        row = cur.fetchone()
        return row[0] if row else 0

    def get_toe_kick_cost(self):
        return round(4 * self.width / 144 * 14) if self.toe_kick == "Yes" else 0

    def get_end_panel_cost(self):
        return round(self.width * 36 / 144 * 10) if self.end_panel == "Yes" else 0

    def get_finish_cost(self):
        cur = self.conn.cursor()
        cur.execute("SELECT price FROM finishes WHERE collection=? AND finish=?", (self.collection, self.finish))
        row = cur.fetchone()
        return row[0] if row else 0

    def calculate_total_cost(self):
        if self.location == 'Vanity':
            total = (
                self.collection_cost_value +
                self.location_cost_value +
                self.drawer_wood_cost_value +
                self.num_drawers_cost_value +
                self.num_doors_cost_value +
                self.frame_wood_cost_value +
                self.finish_cost_value
            )
        else:
            base_cost = (
                (self.total_collection_cost() +
                self.location_cost_value +
                self.carcass_cost_value +
                self.drawer_wood_cost_value +
                self.num_drawers_cost_value +
                self.num_doors_cost_value +
                self.frame_wood_cost_value +
                self.toe_kick_cost_value +
                self.glass_cost_value +
                self.finish_cost_value +
                self.end_panel_cost_value
            ))
            print(f"Collection Cost: {self.total_collection_cost()}")
            print(f"Location Cost: {self.location_cost_value}")
            print(f"Carcass Int Cost: {self.carcass_cost_value}")
            print(f"Drawer Wood: {self.drawer_wood_cost_value}")
            print(f"Num Drawers Cost : {self.num_drawers_cost_value}")
            print(f"Num Doors Cost: {self.num_doors_cost_value}")
            print(f"Wood Frame Cost: {self.frame_wood_cost_value}")
            print(f"Toe Kick: {self.toe_kick_cost_value}")
            print(f"Glass Cost: {self.glass_cost_value}")
            print(f"Finish Cost: {self.finish_cost_value}")
            print(f"Base cost: {base_cost}")
            
            width_factor = self.width_cost_value
            print(f"Width factor: {width_factor}")

            hinge_style_cost = self.hinge_style_cost
            print(f"Hinge style cost: {hinge_style_cost}")

            ceiling_height_cost = self.ceiling_height_cost
            print(f"Ceiling height cost: {ceiling_height_cost}")

            back_panel_cost = self.back_panel_cost_value
            print(f"Back panel cost: {back_panel_cost}")

            total = base_cost * width_factor
            total *= hinge_style_cost
            total *= ceiling_height_cost
            total *= back_panel_cost
            print(f"Total after applying multipliers: {total}")

        return total
    
    def calculate_materials(self):
        # Assuming plywood sheet dimensions are 4 feet by 8 feet
        sheet_width = 4 * 12  # in inches
        sheet_height = 8 * 12  # in inches
        sheet_area = sheet_width * sheet_height  # in square inches

        # Calculate the total area required for the cabinet
        side_area = 2 * (self.width * self.height)
        top_bottom_area = 2 * (self.width * self.depth)
        back_area = self.width * self.height
        shelf_area = self.num_drawers * (self.width * self.depth)

        total_area = side_area + top_bottom_area + back_area + shelf_area
        num_sheets = total_area / sheet_area

        return {
            'total_area': total_area,
            'num_sheets': num_sheets
        }

cabinets_list = []

@app.route('/')
def index():
    print("Rendering index.html")
    return render_template('index.html')

@app.route('/estimate', methods=['GET', 'POST'])
def estimate():
    total_cost = None
    if request.method == 'POST':
        collection = request.form['collection']
        location = request.form['location']
        width = int(request.form['width'])
        carcass_interior = request.form['carcass_interior']
        drawer_wood = request.form['drawer_wood']
        hinge_style = request.form['hinge_style']
        ceiling_height = int(request.form['ceiling_height'])
        num_drawers = int(request.form['num_drawers'])
        num_doors = int(request.form['num_doors'])
        frame_wood = request.form['frame_wood']
        glass = request.form['glass']
        back_panel = request.form['back_panel']
        toe_kick = request.form['toe_kick']
        end_panel = request.form['end_panel']
        finish = request.form['finish']

        conn = get_db_connection()
        cabinet = Cabinet(conn, collection, location, width, carcass_interior, drawer_wood, hinge_style, ceiling_height, num_drawers, num_doors, frame_wood, glass, back_panel, toe_kick, end_panel, finish)
        total_cost = cabinet.calculate_total_cost()
        conn.close()

        cabinets_list.append({
            'collection': collection,
            'location': location,
            'width': width,
            'carcass_interior': carcass_interior,
            'drawer_wood': drawer_wood,
            'hinge_style': hinge_style,
            'ceiling_height': ceiling_height,
            'num_drawers': num_drawers,
            'num_doors': num_doors,
            'frame_wood': frame_wood,
            'glass': glass,
            'back_panel': back_panel,
            'toe_kick': toe_kick,
            'end_panel': end_panel,
            'finish': finish,
            'total_cost': total_cost
        })

    # Calculate the total cost of all cabinets
    total_cost_all_cabinets = sum(cabinet['total_cost'] for cabinet in cabinets_list)

    return render_template('estimate.html', total_cost=total_cost, cabinets=cabinets_list, total_cost_all_cabinets=total_cost_all_cabinets)

@app.route('/edit/<int:index>', methods=('GET', 'POST'))
def edit(index):
    if request.method == 'POST':
        collection = request.form['collection']
        location = request.form['location']
        width = int(request.form['width'])
        carcass_interior = request.form['carcass_interior']
        drawer_wood = request.form['drawer_wood']
        hinge_style = request.form['hinge_style']
        ceiling_height = int(request.form['ceiling_height'])
        num_drawers = int(request.form['num_drawers'])
        num_doors = int(request.form['num_doors'])
        frame_wood = request.form['frame_wood']
        glass = request.form['glass']
        back_panel = request.form['back_panel']
        toe_kick = request.form['toe_kick']
        end_panel = request.form['end_panel']
        finish = request.form['finish']

        conn = get_db_connection()
        cabinet = Cabinet(conn, collection, location, width, carcass_interior, drawer_wood, hinge_style, ceiling_height, num_drawers, num_doors, frame_wood, glass, back_panel, toe_kick, end_panel, finish)
        cabinet_cost = cabinet.calculate_total_cost()
        conn.close()

        # Update the cabinet in the list
        cabinets_list[index] = {
            'collection': collection,
            'location': location,
            'width': width,
            'carcass_interior': carcass_interior,
            'drawer_wood': drawer_wood,
            'hinge_style': hinge_style,
            'ceiling_height': ceiling_height,
            'num_drawers': num_drawers,
            'num_doors': num_doors,
            'frame_wood': frame_wood,
            'glass': glass,
            'back_panel': back_panel,
            'toe_kick': toe_kick,
            'end_panel': end_panel,
            'finish': finish,
            'total_cost': cabinet_cost
        }

        total_cost = sum(cabinet['total_cost'] for cabinet in cabinets_list)
        return redirect(url_for('estimate'))

    cabinet = cabinets_list[index]

    return render_template('edit.html', index=index, cabinet=cabinet)

@app.route('/delete/<int:index>', methods=['POST'])
def delete(index):
    if 0 <= index < len(cabinets_list):
        del cabinets_list[index]
    # Recalculate the total cost of all cabinets
    total_cost_all_cabinets = sum(cabinet['total_cost'] for cabinet in cabinets_list)
    
    return redirect(url_for('estimate', total_cost_all_cabinets=total_cost_all_cabinets))

@app.route('/render', methods=['GET', 'POST'])
def render():
    pass
    return render_template('render.html')

customers = []

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        customer_id = len(customers) + 1
        customer = Customer(customer_id, name, email)
        customers.append(customer)
        return redirect(url_for('list_customers'))
    return render_template('add_customer.html')

@app.route('/list_customers')
def list_customers():
    return render_template('list_customers.html', customers=customers)

@app.route('/add_job/<int:customer_id>', methods=['GET', 'POST'])
def add_job(customer_id):
    customer = next((c for c in customers if c.customer_id == customer_id), None)
    if customer is None:
        return "Customer not found", 404

    if request.method == 'POST':
        # Job details
        job_name = request.form['job_name']
        job_address = request.form['job_address']
        job_notes = request.form['job_notes']
        customer_name = request.form['customer_name']
        customer_email = request.form['customer_email']
        phone = request.form['phone']
        secondary_contact1 = request.form['secondary_contact1']
        secondary_contact2 = request.form['secondary_contact2']

        # Cabinet details
        collection = request.form['collection']
        location = request.form['location']
        width = int(request.form['width'])
        carcass_interior = request.form['carcass_interior']
        drawer_wood = request.form['drawer_wood']
        hinge_style = request.form['hinge_style']
        ceiling_height = int(request.form['ceiling_height'])
        num_drawers = int(request.form['num_drawers'])
        num_doors = int(request.form['num_doors'])
        frame_wood = request.form['frame_wood']
        glass = request.form['glass']
        back_panel = request.form['back_panel']
        toe_kick = request.form['toe_kick']
        end_panel = request.form['end_panel']
        finish = request.form['finish']

        conn = get_db_connection()
        cabinet = Cabinet(conn, collection, location, width, carcass_interior, drawer_wood, hinge_style, ceiling_height, num_drawers, num_doors, frame_wood, glass, back_panel, toe_kick, end_panel, finish)
        total_cost = cabinet.calculate_total_cost()
        materials = cabinet.calculate_materials()
        conn.close()

        job = {
            'job_name': job_name,
            'job_address': job_address,
            'job_notes': job_notes,
            'customer_name': customer_name,
            'customer_email': customer_email,
            'phone': phone,
            'secondary_contact1': secondary_contact1,
            'secondary_contact2': secondary_contact2,
            'cabinet': cabinet,
            'total_cost': total_cost,
            'materials': materials
        }
        customer.add_job(job)

        return redirect(url_for('view_customer', customer_id=customer_id))

    return render_template('add_job.html', customer=customer)


@app.route('/view_customer/<int:customer_id>')
def view_customer(customer_id):
    customer = next((c for c in customers if c.customer_id == customer_id), None)
    if customer is None:
        return "Customer not found", 404
    return render_template('view_customer.html', customer=customer)

@app.route('/login')
def user_login():
    return render_template('login.html')

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True)
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)


