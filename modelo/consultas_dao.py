from .coneciondb import Conneccion

def crear_tabla():
    conn = Conneccion()

    sql1= '''
        CREATE TABLE IF NOT EXISTS Genero(
        ID INTEGER NOT NULL,
        Nombre VARCHAR(50),
        PRIMARY KEY (ID AUTOINCREMENT)
        );
    '''

    sql2= '''
            CREATE TABLE IF NOT EXISTS Director(
            ID INTEGER NOT NULL,
            Nombre VARCHAR(100),
            PRIMARY KEY (ID AUTOINCREMENT)
            );
    '''
    
    sql3= '''
            CREATE TABLE IF NOT EXISTS Anio(
            ID INTEGER NOT NULL,
            Anio INTEGER,
            PRIMARY KEY (ID AUTOINCREMENT)
            );
    '''

    sql4 = '''
    CREATE TABLE IF NOT EXISTS Peliculas(
            ID INTEGER NOT NULL,
            Nombre VARCHAR(150),
            Duracion VARCHAR(4),
            Genero INTEGER,
            Director INTEGER,
            Anio INTEGER,
            PRIMARY KEY (ID AUTOINCREMENT),
            FOREIGN KEY (Genero) REFERENCES Genero(ID)
            FOREIGN KEY (Director) REFERENCES Director(ID),
            FOREIGN KEY (Anio) REFERENCES Anio(ID)
            );
    '''
    try:
        for sql in [sql1, sql2, sql3, sql4]:
            conn.cursor.execute(sql)
            conn.cerrar_con()
            conn = Conneccion()

    except:
        pass

class Peliculas():

    def __init__(self,nombre,duracion,genero,director, anio):
       self.nombre = nombre
       self.duracion = duracion
       self.genero = genero
       self.director = director
       self.anio = anio

    def __str__(self):
        return f'Pelicula[{self.nombre},{self.duracion},{self.genero},{self.director}, {self.anio}]'
    
def guardar_peli(pelicula):
    conn = Conneccion()

    sql= f'''
        INSERT INTO Peliculas(Nombre,Duracion,Genero, Director, Anio)
        VALUES('{pelicula.nombre}','{pelicula.duracion}',{pelicula.genero}, {pelicula.director}, {pelicula.anio});
'''
    try:
        conn.cursor.execute(sql)
        conn.cerrar_con()
    except:
        pass

def listar_peli():
    conn = Conneccion()
    listar_peliculas = []

    sql= f'''
        SELECT p.ID,p.Nombre,p.Duracion, g.Nombre, d.Nombre, a.Anio FROM Peliculas as p
        INNER JOIN Genero as g
        ON p.Genero = g.ID;
        
        INNER JOIN Director as d
        ON p.Director = d.ID;
        
        INNER JOIN Anio as a
        ON p.Anio = a.ID;
'''
    try:
        conn.cursor.execute(sql)
        listar_peliculas = conn.cursor.fetchall()
        conn.cerrar_con()
        #print(listar_peliculas)
        return listar_peliculas
    except:
        pass

def listar_generos():
    conn = Conneccion()
    listar_genero = []

    sql= f'''
        SELECT * FROM Genero;
'''
    try:
        conn.cursor.execute(sql)
        listar_genero = conn.cursor.fetchall()
        conn.cerrar_con()

        return listar_genero
    except:
        pass
    
def listar_directores():
    conn = Conneccion()
    try:
        conn.cursor.execute("SELECT * FROM Director;")
        return conn.cursor.fetchall()
    finally:
        conn.cerrar_con()

def listar_anios():
    conn = Conneccion()
    try:
        conn.cursor.execute("SELECT * FROM Anio;")
        return conn.cursor.fetchall()
    finally:
        conn.cerrar_con()


def editar_peli(pelicula, id):
    conn = Conneccion()

    sql= f'''
        UPDATE Peliculas
        SET Nombre = '{pelicula.nombre}', 
            Duracion = '{pelicula.duracion}', 
            Genero = {pelicula.genero},
            Director = {pelicula.director},
            Anio = {pelicula.anio}
        WHERE ID = {id}
        ;
'''
    try:
        conn.cursor.execute(sql)
        conn.cerrar_con()
    except:
        pass

def borrar_peli(id):
    conn = Conneccion()

    sql= f'''
        DELETE FROM Peliculas
        WHERE ID = {id}
        ;
'''
    try:
        conn.cursor.execute(sql)
        conn.cerrar_con()
    except:
        pass