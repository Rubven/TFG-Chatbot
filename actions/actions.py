# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


#modificado de: https://rasa.com/docs/action-server/sdk-actions
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction

import mysql.connector
mydb = mysql.connector.connect(
	user='rasa',
	password='rasapwd',
	host='localhost',
	database='chatbot_db',
	auth_plugin='mysql_native_password',
)
mycursor = mydb.cursor()


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

		return []


class ActionListaAcciones(Action):
	def name(self) -> Text:
		return "action_lista_acciones"
		
	def run(self,
			dispatcher: CollectingDispatcher,
			tracker: Tracker,
			domain):
			
		acciones = [
			'Saludar',
			'Despedir',
			'Ver acciones',
			'Ver asignaturas',
			'Registrar usuario',
			'Registrar usuario en asignatura (desarrollo -> botones)',
			'Consultar horario asignatura (desarrollo -> botones)'
			
		]

		for accion in acciones:
			dispatcher.utter_message(accion)
		return []


class ActionUsuarioExiste(Action):
	def name(self) -> Text:
		return "action_usuario_existe"
	
	def run(self,
			dispatcher,
			tracker: Tracker,
			domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

		# Store uid
		uid = tracker.sender_id

		q = ("SELECT COUNT(*) FROM usuario WHERE usuario.id='{}'".format(uid))
		mycursor.execute(q)
		result = mycursor.fetchall()
		mycursor.reset()

		if result[0][0] >= 1:
			#return[SlotSet("usuario_existe", True), FollowupAction("utter_greet_user")]
			
			# Coger nombre y setearlo
			q = ("SELECT nombre FROM usuario WHERE usuario.id='{}'".format(uid))
			mycursor.execute(q)
			result = mycursor.fetchall()
			mycursor.reset()
			return[SlotSet("usuario_existe", True), SlotSet("nombre_usuario", result[0][0])]

		else:
			#return[SlotSet("usuario_existe", False), FollowupAction("utter_introduce")]
			return[SlotSet("usuario_existe", False)]


class ActionGuardarNombreUsuario(Action):
	def name(self) -> Text:
		return "action_guardar_nombre_usuario"
	
	def run(self,
			dispatcher,
			tracker: Tracker,
			domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

		uid = tracker.sender_id	
		nombre = tracker.get_slot('nombre_usuario')
		
		q = ("INSERT INTO usuario (id, nombre) VALUES ('{uid}','{nombre}')".format(uid=uid, nombre=nombre))
		mycursor.execute(q)
		mydb.commit()
		mycursor.reset()

		return []

class ActionListaAsignaturasRegistrado(Action):
	def name(self) -> Text:
		return "action_lista_asignaturas_registrado"
		
	def run(self,
			dispatcher: CollectingDispatcher,
			tracker: Tracker,
			domain):
			
		uid = tracker.sender_id	
		
		q = ("""SELECT nombre 
				FROM asignatura, usuario, usuario-asignatura 
				WHERE asignatura.id = usuario-asignatura.asignatura_id
				AND asignatura.curso='2020-2021'
				AND usuario.id = usuario-asignatura.usuario_id 
				AND usuario.id = '{}'""".format(uid))
		
		mycursor.execute(q)
		result = mycursor.fetchall()

		for item in result:
			dispatcher.utter_message(item[0])
		mycursor.reset()

		return []