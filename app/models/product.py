from app.db import get_db

class ProductItem:
    def __init__(self, product_id, name, description, price):
        self.product_id = product_id
        self.name = name
        self.description = description
        self.price = price


    def UpdateDatabase(self):
        db = get_db()
        sql = """UPDATE products SET name = ?, description = ?, price = ? WHERE product_id = ?;"""
        db.execute(sql, [self.name, self.description, self.price, self.product_id])
        db.commit()
        
    def Delete(self):
        db = get_db()
        sql = """DELETE FROM products WHERE product_id = ?;"""
        db.execute(sql, [self.product_id])
        db.commit()
        
    @staticmethod
    def GetAll():
        db = get_db()
        sql = "SELECT * FROM products;"
        results = db.execute(sql).fetchall()

        out = []
        for r in results:
            dev = ProductItem.FromDBRow(r)
            if dev is None:
                continue
            out.append(dev)
        return out
        
    @staticmethod
    def Create(name, description, price):
        db = get_db()
        sql = """INSERT INTO products (name, description, price) VALUES (?, ?, ?);"""
        cursor = db.execute(sql, [name, description, price])
        id = cursor.lastrowid
        db.commit()
        return ProductItem.FromDB(id)
        
    @staticmethod
    def FromDBRow(row):
        if row is None:
            return None
        return ProductItem(
        product_id=row['product_id'],   # or whatever your actual DB field name is
        name=row['name'],
        description=row['description'],       # make sure this matches your DB schema!
        price=row['price']
    )
    
    @staticmethod
    def FromDB(id : int):
        db = get_db()
        sql = "SELECT * FROM products WHERE product_id = ?;"
        result = db.execute(sql, [id]).fetchone()
        return ProductItem.FromDBRow(result)