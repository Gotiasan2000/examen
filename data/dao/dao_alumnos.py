from data.modelo.alumno import Alumno

class DaoAlumnos:
    
    def get_all(self,db) -> list[Alumno]:
        cursor = db.cursor()
    
        cursor.execute("SELECT * FROM alumnos")

        equipos_en_db = cursor.fetchall()
        equipos : list[Alumno]= list()
        for equipo in equipos_en_db:
            alumno = Alumno(equipo[0], equipo[1])
            equipos.append(alumno)
        cursor.close()
        
        return equipos
    
    def insert(self, db, nombre: str):
        cursor = db.cursor()
        sql = ("INSERT INTO alumnos (nombre) values (%s) ")
        data = (nombre,)
        cursor.execute(sql,data)
        # cursor.execute(f"INSERT INTO alumnos (nombre) VALUES ('{nombre}')")
        db.commit()
        cursor.close()

    def delete(self, db, id: str):
        cursor = db.cursor()
        sql = ("DELETE FROM  alumnos where id = (%s) ")
        data = (id,)
        cursor.execute(sql,data)
        # cursor.execute(f"INSERT INTO alumnos (nombre) VALUES ('{nombre}')")
        db.commit()
        cursor.close()