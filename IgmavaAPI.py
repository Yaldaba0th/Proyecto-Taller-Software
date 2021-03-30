from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask import jsonify
import random

db_connect = create_engine('mysql+pymysql://root:@127.0.0.1/igmava')
app = Flask(__name__)
api = Api(app)

class Clientes(Resource):
    def get(self):
        conn = db_connect.connect() # connect to database
        query = conn.execute("select * from Cliente") # This line performs query and returns json result
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

    def post(self):
        data = request.json
        conn = db_connect.connect()
        query = conn.execute("insert into Cliente values ('{}', '{}', '{}', {}, '{}', '{}')".format(
                             data['RUT'],
                             data['nombre'],
                             data['procedencia'],
                             int(data['telefono']),
                             data['correo'],
                             data['contacto']))
        return jsonify({'message': '0'})

class Clientes_rut(Resource):
    def get(self, rut):
        conn = db_connect.connect()
        query = conn.execute("select * from Cliente where RUT='%s'" %rut)
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

    def delete(self, rut):
        conn = db_connect.connect()
        query = conn.execute("delete from Cliente where RUT='%s'" %rut)
        return jsonify({'message': '0'})

    def put(self, rut):
        data = request.json
        conn = db_connect.connect()
        query = conn.execute("update Cliente set nombre='{}', procedencia='{}', telefono={}, correo='{}', contacto='{}' where RUT='{}'".format(
                             data['nombre'],
                             data['procedencia'],
                             int(data['telefono']),
                             data['correo'],
                             data['contacto'],
                             rut))
        return 0
        
class Cabins(Resource):
    def get(self):
        conn = db_connect.connect() # connect to database
        query = conn.execute("select * from Cabin") # This line performs query and returns json result
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

class Cabins_id(Resource):
    def get(self, _id):
        conn = db_connect.connect()
        query = conn.execute("select * from Cabin where ID=%d " %int(_id))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)
    
    def put(self, _id):
        data = request.json
        conn = db_connect.connect()
        query = conn.execute("update Cabin set Precio={}, Observaciones='{}'  where ID={}".format(
                             data['precio'],
                             data['observaciones'],
                             int(_id)))
        return 0
class Cabins_precio(Resource):
    def put(self):
        data = request.json
        conn = db_connect.connect()
        for ids in [1,2,3]:
            query = conn.execute("update Cabin set Precio={} where ID={}".format(int(data['precio']), ids))
        return 0


class Observaciones_id(Resource):
    def get(self, _id): # cab id
        conn = db_connect.connect()
        query = conn.execute("select * from ObsCab where Cabin=%d " %int(_id))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

    def delete(self, _id):
        conn = db_connect.connect()
        query = conn.execute("delete from ObsCab where ID=%d" %int(_id))
        return 0

    def put(self, _id): # ons id
        data = request.json
        conn = db_connect.connect()
        query = conn.execute("update ObsCab set Cabin={}, Tipo='{}', Fecha='{}', Descripcion='{}', Arreglado={}  where ID={}".format(
                             data['cabin'],
                             data['tipo'],
                             data['fecha'],
                             data['descripcion'],
                             data['arreglado'],
                             int(_id)))

class Observaciones_no_arreglado(Resource):
    def get(self, _id): # cab id
        conn = db_connect.connect()
        query = conn.execute("select * from ObsCab where Cabin=%d and Arreglado=0" %int(_id))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)


class Observaciones(Resource):
    def post(self):
        id_ = random.randint(0,1000000000) # Hay un problema en mysql y no funcionan indices con autoincremento
        data = request.json
        conn = db_connect.connect()
        query = conn.execute("insert into ObsCab values ({}, {}, '{}', '{}', '{}', {})".format(
                             id_,
                             data['cabin'],
                             data['tipo'],
                             data['fecha'],
                             data['descripcion'],
                             data['arreglado']))
        return 0

class Reservas(Resource):
    def get(self):
        conn = db_connect.connect() # connect to database
        query = conn.execute("select * from Reserva") # This line performs query and returns json result
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

    def post(self):
        id_ = random.randint(0,1000000000) # Hay un problema en mysql y no funcionan indices con autoincremento
        data = request.json
        conn = db_connect.connect()
        query = conn.execute("insert into Reserva values ({}, '{}', '{}', '{}', {}, {})".format(
                             id_,
                             data['RUT'],
                             data['in'],
                             data['out'],
                             int(data['costo']),
                             int(data['pagado'])))
        for cab in data['cabins']:
            query = conn.execute("insert into CabsRes values ({}, {})".format(
                             id_, cab))
        return 0

class Reservas_id(Resource):
    def get(self, _id):
        conn = db_connect.connect()
        query = conn.execute("select * from Reserva where ID=%d" %int(_id))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        query = conn.execute("select IDcabin from CabsRes where IDreserva=%d" %int(_id))
        result['data'][0]['Cabins'] = [i[0] for i in query.cursor]
        return jsonify(result)

    def delete(self, _id):
        conn = db_connect.connect()
        query = conn.execute("delete from CabsRes where IDreserva=%d" %int(_id))
        query = conn.execute("delete from Reserva where ID=%d" %int(_id))
        return 0

    def put(self, _id):
        data = request.json
        conn = db_connect.connect()
        query = conn.execute("update Reserva set rut='{}', check_in='{}', check_out='{}', costo={}, pagado={} where id={}".format(
                             data['RUT'],
                             data['in'],
                             data['out'],
                             int(data['costo']),
                             int(data['pagado']),
                             int(_id)))
        query = conn.execute("delete from CabsRes where IDreserva=%d" %int(_id))
        for cab in data['cabins']:
            query = conn.execute("insert into CabsRes values ({}, {})".format(
                             _id, cab))
        return 0

class Reservas_rut(Resource):
    def get(self, _rut):
        conn = db_connect.connect()
        query = conn.execute("select * from Reserva where RUT='{}'".format(_rut))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        print(result)
        return jsonify(result)

class Reservas_date(Resource):
    def get(self, date):
        conn = db_connect.connect()
        query = conn.execute("select * from Reserva where check_out >= '%s'" %date)
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)


class Reservas_ocupadas(Resource):
    def get(self, date):
        conn = db_connect.connect()
        query = conn.execute("select IDcabin, Nombre, Cliente.RUT, Procedencia, Telefono, Correo, Contacto from CabsRes left join Reserva on CabsRes.IDreserva = Reserva.Id left join Cliente on Reserva.RUT = Cliente.RUT where Check_out >= '{}' and Check_in <= '{}'".format(date, date))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)



class Reservas_nopagadas(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from Reserva where pagado=0")
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

class Disponible(Resource):
    def get(self, a, b):
        conn = db_connect.connect()
	# select ID from Cabin where ID not in (select IDcabin from CabsRes)
        query = conn.execute("select ID from Cabin where Id not in (select IDcabin from CabsRes left join Reserva on CabsRes.IDreserva = Reserva.Id where Check_out >= '{}' and Check_in <= '{}')".format(a,b))
        result = {'data': [{'Cabins': [i[0] for i in query.cursor]}]}
        return jsonify(result)


api.add_resource(Clientes, '/clientes')
api.add_resource(Clientes_rut, '/clientes/<rut>') 
api.add_resource(Cabins, '/cabanas')
api.add_resource(Cabins_id, '/cabanas/<_id>') 
api.add_resource(Observaciones, '/observaciones/') 
api.add_resource(Observaciones_no_arreglado, '/noarreglado/<_id>') 
api.add_resource(Observaciones_id, '/observaciones/<_id>') 
api.add_resource(Reservas, '/reservas')
api.add_resource(Reservas_id, '/reservas/<_id>')
api.add_resource(Reservas_rut, '/reservasRut/<_rut>')
api.add_resource(Reservas_date, '/fecha/<date>') 
api.add_resource(Reservas_nopagadas, '/nopagado') 
api.add_resource(Disponible, '/disponible/<a>/<b>') 
api.add_resource(Reservas_ocupadas, '/ocupado/<date>')
api.add_resource(Cabins_precio, '/cabanas/precio')


if __name__ == '__main__':
     app.run(port='8007')
        
        
#Ejemplos para tests:
#curl 127.0.0.1:8007/clientes
#curl 127.0.0.1:8007/clientes/9345872
#curl -X POST -d '{"id":"4", "nombre":"Juan"}' -H "Content-Type: application/json" 127.0.0.1:8007/clientes
#curl -X DELETE 127.0.0.1:8007/clientes/1
#curl -X PUT -d '{"nombre":"Iris"}' -H "Content-Type: application/json" 127.0.0.1:8007/clientes/1

#curl 127.0.0.1:8007/cabanas
#curl -X PUT -d '{"estado":1}' -H "Content-Type: application/json" 127.0.0.1:8007/cabanas/1

#curl 127.0.0.1:8007/reservas

