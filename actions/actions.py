# Modificado de: https://rasa.com/docs/action-server/sdk-actions
from typing import Any, Text, Dict, List, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.forms import FormValidationAction
import json


# Conexión a BD MYSQL, con credenciales del servidor
import mysql.connector
mydb = mysql.connector.connect(
	user='rasa',
	password='rasapwd',
	host='localhost',
	database='chatbot_db',
	auth_plugin='mysql_native_password',
)
mycursor = mydb.cursor()


# Conexión a MongoDB
import pymongo
client = pymongo.MongoClient("localhost", 27017)
mongodb = client["preguntas"]


# Consulta que devuelve el nombre de todas las asignaturas
class ActionVerAsignaturas(Action):
	def name(self) -> Text:
		return "action_ver_asignaturas"
		
	def run(self,
			dispatcher: CollectingDispatcher,
			tracker: Tracker,
			domain):
			
		q = "SELECT nombre FROM asignatura"
		mycursor.execute(q)
		result = mycursor.fetchall()

		for item in result:
			dispatcher.utter_message(item[0])
		mycursor.reset()


# Devuelve lista de acciones que puede realizar el bot
class ActionListaAcciones(Action):
	def name(self) -> Text:
		return "action_lista_acciones"
		
	def run(self,
			dispatcher: CollectingDispatcher,
			tracker: Tracker,
			domain):
			
		acciones = [
			'- Saludar',
			'- Despedir',
			'- Mostrarr acciones',
			'- Registrar usuario',
			'- Registrar usuario en asignatura',
			'- Consultar horario asignatura (en desarrollo)',
			'- Hacer preguntas de asignaturas'	
		]

		for accion in acciones:
			dispatcher.utter_message(accion)


# Consulta en BD si el usuario existe y devuelve un booleano. 
# Si el usuario existe, devuelve también el nombre.
class ActionUsuarioExiste(Action):
	def name(self) -> Text:
		return "action_usuario_existe"
	
	def run(self,
			dispatcher,
			tracker: Tracker,
			domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

		uid = tracker.sender_id
		
		# Control de errores
		if uid != None:
			q = ("SELECT COUNT(*) FROM usuario WHERE usuario.id='{}'".format(uid))
			mycursor.execute(q)
			result = mycursor.fetchall()
			mycursor.reset()

			# Si la consulta devuelve al menos un resultado, mirar el nombre para devolverlo
			if result[0][0] >= 1:
				q = ("SELECT nombre FROM usuario WHERE usuario.id='{}'".format(uid))
				mycursor.execute(q)
				result = mycursor.fetchall()
				mycursor.reset()
				return[SlotSet("usuario_existe", 1.0), SlotSet("nombre_usuario", result[0][0])]

			else:
				return[SlotSet("usuario_existe", 0.0)]
			

# Guardar en base de datos el nombre proporcionado por el usuario
class ActionGuardarNombreUsuario(Action):
	def name(self) -> Text:
		return "action_guardar_nombre_usuario"
	
	def run(self,
			dispatcher,
			tracker: Tracker,
			domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

		uid = tracker.sender_id	
		nombre = tracker.get_slot('nombre_usuario')
		
		# Control de errores
		if uid != None and nombre != None:

			# Comprobar si el usuario existe:
			q = ("SELECT * FROM usuario WHERE usuario.id='{}'".format(uid))
			mycursor.execute(q)
			result = mycursor.fetchall()
			mycursor.reset()

			if len(result) != 0:
				dispatcher.utter_message("Error: el usuario ya existe")
				
			else:
				q = ("""INSERT IGNORE INTO usuario (id, nombre) VALUES ('{uid}','{nombre}');""".format(uid=uid, nombre=nombre))
				mycursor.execute(q)
				mydb.commit()
				mycursor.reset()


# Devuelve lista de asignaturas a las que está registrado el usuario
class ActionListaAsignaturasRegistrado(Action):
	def name(self) -> Text:
		return "action_lista_asignaturas_registrado"
		
	def run(self,
			dispatcher: CollectingDispatcher,
			tracker: Tracker,
			domain):
			
		uid = tracker.sender_id	

		# Control de errores
		if uid != None:
			q = ("""SELECT nombre 
					FROM asignatura, usuario, usuario_asignatura 
					WHERE asignatura.codigo = usuario_asignatura.asignatura_codigo
					AND usuario.id = usuario_asignatura.usuario_id 
					AND usuario.id = '{}'""".format(uid))
			
			mycursor.execute(q)
			result = mycursor.fetchall()

			for item in result:
				dispatcher.utter_message(item[0])
			mycursor.reset()
		
		else:
			dispatcher.utter_message("No hay ninguna asignatura registrada")


# Devuelve lista de asignaturas de un curso concreto
class ActionListaAsignaturasAnyo(Action):
	def name(self) -> Text:
		return "action_lista_asignaturas_anyo"
		
	def run(self,
			dispatcher: CollectingDispatcher,
			tracker: Tracker,
			domain):
			
		anyo = tracker.get_slot('anyo')	

		# Control de errores
		if anyo != None:	
			q = ("""SELECT nombre 
					FROM asignatura
					WHERE asignatura.anyo LIKE '%{}%';""".format(anyo))
			
			mycursor.execute(q)
			result = mycursor.fetchall()

			if len(result) == 0:
				dispatcher.utter_message("No hay asignaturas de ese año")

			else:
				dispatcher.utter_message("Selecciona a qué asignatura quieres registrarte:")
				for item in result:
					dispatcher.utter_message(item[0])

			mycursor.reset()


# Devuelve la lista de asignaturas del curso especificado en formato button
# para que el usuario pueda registrarse en la que seleccione
class ActionListaAsignaturasAnyoButton(Action):
	def name(self) -> Text:
		return "action_lista_asignaturas_anyo_button"
		
	def run(self,
			dispatcher: CollectingDispatcher,
			tracker: Tracker,
			domain):
			
		anyo = tracker.get_slot('anyo')	
		if anyo != None:
			q = ("""SELECT nombre, codigo 
					FROM asignatura
					WHERE asignatura.anyo LIKE '%{}%';""".format(anyo))
			
			mycursor.execute(q)
			result = mycursor.fetchall()

			if len(result) == 0:
				dispatcher.utter_message("No hay asignaturas de ese año")

			else:
				mybuttons = []
				for item in result:
					slotname={ "asignatura_codigo": item[1]}
					json_slotname = json.dumps(slotname)
					button={"title":item[0], "payload":"/registrar_asignatura_codigo{}".format(json_slotname)}
					mybuttons.append(button)

				dispatcher.utter_message("Asignaturas año {}:".format(anyo), buttons= mybuttons)
				
			mycursor.reset()


# Dados un UID y CODIGO_ASIGNATURA, da de alta la relación en BD
class ActionRegistrarAsignaturaCodigo(Action):
	def name(self) -> Text:
		return "action_registrar_asignatura_codigo"
		
	def run(self,
			dispatcher: CollectingDispatcher,
			tracker: Tracker,
			domain):
			
		uid = tracker.sender_id
		codigo = tracker.get_slot('asignatura_codigo')

		# Control de errores
		if codigo != None:	

			q = ("""SELECT asignatura.nombre 
					FROM asignatura, usuario, usuario_asignatura 
					WHERE asignatura.codigo = usuario_asignatura.asignatura_codigo
					AND usuario.id = usuario_asignatura.usuario_id 
					AND usuario.id = '{uid}'
					AND asignatura.codigo = '{codigo}'""".format(uid=uid, codigo=codigo))
			
			mycursor.execute(q)
			result = mycursor.fetchall()
			
			if len(result) != 0:
				dispatcher.utter_message("Ya estabas registrado en esta asignatura")

			else:
				q = ("""INSERT INTO usuario_asignatura (usuario_id, asignatura_codigo)
						VALUES ('{uid}','{codigo}')""".format(uid=uid, codigo=codigo))
				
				mycursor.execute(q)	
				mydb.commit()
				mycursor.reset()
				dispatcher.utter_message("Registrado")


# Comprueba qué asignaturas tiene registradas el usuario y devuelve una lista para
# que seleccione de cuál quiere preguntas
class ActionListaAsignaturasPreguntas(Action):
	def name(self) -> Text:
		return "action_lista_asignaturas_preguntas"
		
	def run(self,
			dispatcher: CollectingDispatcher,
			tracker: Tracker,
			domain):
			
		uid = tracker.sender_id

		q = ("""SELECT asignatura.nombre, asignatura.codigo 
				FROM asignatura, usuario_asignatura, usuario
				WHERE usuario.id = '{}'
				AND usuario_asignatura.usuario_id = usuario.id
				AND usuario_asignatura.asignatura_codigo = asignatura.codigo""".format(uid))
		
		mycursor.execute(q)
		result = mycursor.fetchall()

		if len(result) == 0:
			dispatcher.utter_message("No tienes asignaturas registradas. Inscríbete primero.")

		else:
			mybuttons = []

			for item in result:
				slotname={ "asignatura_codigo": item[1]}
				json_slotname = json.dumps(slotname)
				button={"title":item[0], "payload":"/preguntas_asignatura_codigo{}".format(json_slotname)}
				mybuttons.append(button)

			dispatcher.utter_message("De qué asignatura quieres que te pregunte?", buttons= mybuttons)
			
		mycursor.reset()


# Genera preguntas al azar de la asignatura especificada de hasta 8 opciones (los casos actuales son todos de 4).
# Contiene la opción de generar preguntas de un tema concreto también.
class ActionPreguntaAsignatura(Action):
	def name(self) -> Text:
		return "action_preguntas_asignatura"
		
	def run(self,
			dispatcher: CollectingDispatcher,
			tracker: Tracker,
			domain):
			
		uid = tracker.sender_id
		codigo = tracker.get_slot('asignatura_codigo')

		# Control de errores
		if codigo != None:
			# Comprobar si hay preguntas de la asignatura
			collist = mongodb.list_collection_names()
			if str(codigo) in collist: 	
				collection = mongodb[str(codigo)]

				# Pregunta al azar
				query = collection.aggregate([{ "$sample": { "size": 1 } }])
				
				# Pregunta de un tema concreto (tema  t = STRING!)
				# query = collection.aggregate([{ "$match": { "tema": "t" }}, {"$sample": { "size": 1 } }])

				result = list(query)
				mybuttons = []
				opciones = ['A', 'B', 'C', 'D', 'F', 'G', 'H', 'I']
				i = 0
				for opcion in result[0]['opciones']:
					slotname={ "respuesta_correcta": opcion['isCorrect']}
					json_slotname = json.dumps(slotname)
					button={"title":opciones[i], "payload":"/contestar_pregunta{}".format(json_slotname)}
					mybuttons.append(button)
					i += 1

				i = 0
				dispatcher.utter_message("Pregunta número {}:\n{}".format(result[0]['numPregunta'], result[0]['enunciado']))
				for opcion in result[0]['opciones']:	
					dispatcher.utter_message('{}: '.format(opciones[i])+opcion['opcion'])
					i += 1
				dispatcher.utter_message('Selecciona la respuesta correcta:',buttons=mybuttons)
				return[SlotSet("num_pregunta", result[0]['numPregunta'])]
			
			else:
				dispatcher.utter_message("No hay preguntas de esta asignatura")
	

# Comprueba si la respuesta es correcta o no, devuelve la respuesta correcta en caso de haber fallado
# Y genera botones para decidir si hacer más preguntas o no.
class ActionRespuestaCorrecta(Action):
	def name(self) -> Text:
		return "action_respuesta_correcta"
		
	def run(self,
			dispatcher: CollectingDispatcher,
			tracker: Tracker,
			domain):
			
		uid = tracker.sender_id
		respuesta_correcta = tracker.get_slot('respuesta_correcta')

		# Control de errores
		if respuesta_correcta != None:
			
			if respuesta_correcta:
				dispatcher.utter_message("Respuesta correcta!")
			
			else:
				dispatcher.utter_message("Respuesta incorrecta")

				codigo = tracker.get_slot('asignatura_codigo')
				num_pregunta = tracker.get_slot('num_pregunta')

				if codigo != None and num_pregunta != None:
					collist = mongodb.list_collection_names()
					if str(codigo) in collist: 	
						collection = mongodb[str(codigo)]

						# Respuesta correcta
						x = collection.find({   
							"numPregunta":"{}".format(num_pregunta)},
						{
							"_id":0, "opciones": {"$elemMatch":{ "isCorrect":True}}
						})

						dispatcher.utter_message("La respuesta correcta es: {}".format(x[0]["opciones"][0]["opcion"]))

			# Preguntar si hacer más preguntas		
			codigo = tracker.get_slot('asignatura_codigo')
			slotname={ "asignatura_codigo": codigo}
			json_slotname = json.dumps(slotname)
			buttonYes={"title":"Sí", "payload":"/preguntas_asignatura_codigo{}".format(json_slotname)}
			buttonNo={"title":"No", "payload":"/no_mas_preguntas"}
			mybuttons = []
			mybuttons.append(buttonYes)
			mybuttons.append(buttonNo)
			
			dispatcher.utter_message("Quieres que te haga más preguntas?", buttons=mybuttons)					