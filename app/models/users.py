from flask import g
from app.db import get_db
from werkzeug.security import generate_password_hash, check_password_hash


class User:
    def __init__(self):
        self.id = None
        self.display_name = None
        self.isCritic = False
        self.email = None
        self.passhash = None
        self.role = 1
    
    def CheckPassword(self, password):
        return check_password_hash(self.passhash, password)
    
    def GetPermissions(self):
        db = get_db()
        sql = """ SELECT permissions.name AS permname FROM permissions, role_permissions 
        WHERE role_permissions.roleid = ? AND role_permissions.permissionid = 
        permissions.permissionid; """
        results = db.execute(sql, [self.role]).fetchall()

        out = []
        for r in results:
            out.append(r['permname'])
        return out 
    
    def HasPermission(self, permission):
        return permission in self.GetPermissions()

       
    @staticmethod
    def Create(name, email, password):
        db = get_db()
        sql = """INSERT INTO Users (display_name, email, passhash) VALUES (?, ?, ?);"""
        cursor = db.execute(sql, [name, email, generate_password_hash(password)])
        id = cursor.lastrowid
        db.commit()
        return User.FromDB(id)

    @staticmethod
    def FromDBRow(row):
        if row is None:
            return None
        out = User()
        out.id = row['userid']
        out.display_name = row['display_name']
        out.isCritic = row['is_critic']
        out.email = row['email']
        out.passhash = row['passhash']
        out.role = row['role']
        return out 
    
    @staticmethod
    def FromDB(id : int):
        db = get_db()
        sql = "SELECT * FROM Users WHERE UserId = ?;"
        result = db.execute(sql, [id]).fetchone()
        return User.FromDBRow(result)
    
    @staticmethod
    def FromEmail (email : str):
        db = get_db()
        sql = "SELECT * FROM Users WHERE email = ?;"
        result = db.execute(sql, [email]).fetchone()
        return User.FromDBRow(result)