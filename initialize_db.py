import sqlite3

def create_tables(conn):
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS collections (
        name TEXT PRIMARY KEY,
        price_multiplier REAL
    )''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS locations (
        name TEXT PRIMARY KEY,
        price INTEGER
    )''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS widths (
        width INTEGER PRIMARY KEY,
        factor REAL
    )''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS carcass_materials (
        name TEXT PRIMARY KEY,
        price INTEGER
    )''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS drawer_woods (
        name TEXT PRIMARY KEY,
        price INTEGER
    )''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS hinge_styles (
        name TEXT PRIMARY KEY,
        price_multiplier REAL
    )''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ceiling_heights (
        height INTEGER PRIMARY KEY,
        price_multiplier REAL
    )''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS back_panels (
        name TEXT PRIMARY KEY,
        price_multiplier REAL
    )''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS finishes (
        collection TEXT,
        finish TEXT,
        price INTEGER,
        PRIMARY KEY (collection, finish)
    )''')
    
    conn.commit()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS frame_woods (
        name TEXT PRIMARY KEY,
        price INTEGER
    )''')

def populate_initial_data(conn):
    cursor = conn.cursor()
    
    cursor.execute('INSERT OR IGNORE INTO collections (name, price_multiplier) VALUES ("Shaker", 0.2)')
    cursor.execute('INSERT OR IGNORE INTO collections (name, price_multiplier) VALUES ("English", 0.35)')
    cursor.execute('INSERT OR IGNORE INTO collections (name, price_multiplier) VALUES ("Mill House", 0.3)')
    cursor.execute('INSERT OR IGNORE INTO collections (name, price_multiplier) VALUES ("Regal", 0.4)')
    cursor.execute('INSERT OR IGNORE INTO collections (name, price_multiplier) VALUES ("Governor", 0.32)')
    cursor.execute('INSERT OR IGNORE INTO collections (name, price_multiplier) VALUES ("Diplomat", 0.3)')
    cursor.execute('INSERT OR IGNORE INTO collections (name, price_multiplier) VALUES ("Homestead", 0.35)')
    
    cursor.execute('INSERT OR IGNORE INTO locations (name, price) VALUES ("Base", 350)')
    cursor.execute('INSERT OR IGNORE INTO locations (name, price) VALUES ("Wall", 450)')
    cursor.execute('INSERT OR IGNORE INTO locations (name, price) VALUES ("Tall", 1000)')
    cursor.execute('INSERT OR IGNORE INTO locations (name, price) VALUES ("Countertop", 900)')
    cursor.execute('INSERT OR IGNORE INTO locations (name, price) VALUES ("Freestanding", 1200)')
    cursor.execute('INSERT OR IGNORE INTO locations (name, price) VALUES ("Refrigerator", 1000)')
    cursor.execute('INSERT OR IGNORE INTO locations (name, price) VALUES ("R Front", 600)')
    cursor.execute('INSERT OR IGNORE INTO locations (name, price) VALUES ("DW Front", 100)')
    cursor.execute('INSERT OR IGNORE INTO locations (name, price) VALUES ("Short Wall", 300)')
    cursor.execute('INSERT OR IGNORE INTO locations (name, price) VALUES ("Vanity", 1200)')
    cursor.execute('INSERT OR IGNORE INTO locations (name, price) VALUES ("Sink", 450)')
    cursor.execute('INSERT OR IGNORE INTO locations (name, price) VALUES ("Appliance", 1200)')
    cursor.execute('INSERT OR IGNORE INTO locations (name, price) VALUES ("Open Base", 200)')
    cursor.execute('INSERT OR IGNORE INTO locations (name, price) VALUES ("Open Tall", 350)')
    
    width_factors = {
        9: 1, 10: 1.03, 11: 1.05, 12: 1.07, 13: 1.09, 14: 1.11, 15: 1.13, 
        16: 1.15, 17: 1.17, 18: 1.19, 19: 1.22, 20: 1.24, 21: 1.26, 22: 1.28, 
        23: 1.3, 24: 1.34, 25: 1.36, 26: 1.38, 27: 1.4, 28: 1.42, 29: 1.45, 
        30: 1.56, 31: 1.58, 32: 1.6, 33: 1.62, 34: 1.64, 35: 1.66, 36: 1.78, 
        37: 1.82, 38: 1.88, 39: 1.94, 40: 2.05, 41: 2.13, 42: 2.18, 43: 2.22, 
        44: 2.28, 45: 2.34, 46: 2.38, 47: 2.44, 48: 2.49, 54: 2.54, 60: 2.66, 
        66: 2.75, 72: 2.85
    }
    for width, factor in width_factors.items():
        cursor.execute('INSERT OR IGNORE INTO widths (width, factor) VALUES (?, ?)', (width, factor))
    
    carcass_materials = {
        "Ash (3/4)": 400, "Baltic Birch (3/4)": 400, "Baltic Birch (1/2)": 350, 
        "Cherry (3/4)": 450, "Walnut (3/4)": 500, "White Oak (3/4)": 500
    }
    for name, price in carcass_materials.items():
        cursor.execute('INSERT OR IGNORE INTO carcass_materials (name, price) VALUES (?, ?)', (name, price))
    
    drawer_woods = {
        "Walnut": 12, "Birch": 7, "Maple": 7, "White Oak Qtr Sawn": 14, "White Oak": 12
    }
    for name, price in drawer_woods.items():
        cursor.execute('INSERT OR IGNORE INTO drawer_woods (name, price) VALUES (?, ?)', (name, price))
    
    hinge_styles = {
        "Concealed": 1, "Ball Hinge": 1.2
    }
    for name, price_multiplier in hinge_styles.items():
        cursor.execute('INSERT OR IGNORE INTO hinge_styles (name, price_multiplier) VALUES (?, ?)', (name, price_multiplier))
    
    ceiling_heights = {
        8: 1, 9: 1.1, 10: 1.3
    }
    for height, price_multiplier in ceiling_heights.items():
        cursor.execute('INSERT OR IGNORE INTO ceiling_heights (height, price_multiplier) VALUES (?, ?)', (height, price_multiplier))
    
    back_panels = {
        "Plain": 1, "Shiplap": 1.2, "Woven": 1.4, "Bead Board": 1.1
    }
    for name, price_multiplier in back_panels.items():
        cursor.execute('INSERT OR IGNORE INTO back_panels (name, price_multiplier) VALUES (?, ?)', (name, price_multiplier))
    
    finishes = [
        ("Shaker", "Paint", 125), ("Shaker", "Stain", 100),
        ("English", "Paint", 235), ("English", "Stain", 100),
        ("Mill House", "Paint", 125), ("Mill House", "Stain", 100),
        ("Regal", "Paint", 225), ("Regal", "Stain", 120),
        ("Governor", "Paint", 235), ("Governor", "Stain", 120),
        ("Diplomat", "Paint", 225), ("Diplomat", "Stain", 120),
        ("Homestead", "Paint", 245), ("Homestead", "Stain", 125)
    ]
    for collection, finish, price in finishes:
        cursor.execute('INSERT OR IGNORE INTO finishes (collection, finish, price) VALUES (?, ?, ?)', (collection, finish, price))
    
    frame_woods = {
        "Walnut": 12, "Birch": 7, "Maple": 7, "White Oak Qtr Sawn": 14, 
        "White Oak": 12, "Alder": 7, "Ash": 6, "Hickory": 5, "Cherry": 7
    }
    for name, price in frame_woods.items():
        cursor.execute('INSERT OR IGNORE INTO frame_woods (name, price) VALUES (?, ?)', (name, price))
    

    conn.commit()

def main():
    conn = sqlite3.connect('./cabinets/cabinets.db')
    create_tables(conn)
    populate_initial_data(conn)
    conn.close()

if __name__ == '__main__':
    main()
