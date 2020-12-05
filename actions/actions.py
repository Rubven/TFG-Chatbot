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

<<<<<<< HEAD

#modificado de: https://rasa.com/docs/action-server/sdk-actions
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction

import mysql.connector
c = mysql.connector.connect(
=======
# -------------------------------------------------------------------
# Connect to DB
# -------------------------------------------------------------------
# modificado de: https://rasa.com/docs/action-server/sdk-actions
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

import mysql.connector
c = mysql.connector.connect(	
>>>>>>> 30db7126ea702d15d4c60c60dab46de4ae01319b
	user='rasa',
	password='rasapwd',
	host='localhost',
	database='chatbot_db',
<<<<<<< HEAD
	auth_plugin='mysql_native_password',
)
mycursor = c.cursor()


=======
	auth_plugin='mysql_native_password'
)
#mycursor = c.cursor(buffered=True)
mycursor = c.cursor()

>>>>>>> 30db7126ea702d15d4c60c60dab46de4ae01319b
class ActionVerAsignaturas(Action):
	def name(self) -> Text:
		return "action_ver_asignaturas"
		
<<<<<<< HEAD
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


=======
	
	def run(self,
			dispatcher: CollectingDispatcher,
			tracker: Tracker,
			#domain: Dict[Text, Any]) -> List[Dict[List, Any]]:
			domain):
					
		q = ("SELECT nombre FROM asignaturas")

		mycursor.execute(q)
		result = mycursor.fetchall()
				
		for item in result:
			print(item[0])
			dispatcher.utter_message(item[0])
		
		#return[result if result is not None else []]
		return []



				
>>>>>>> 30db7126ea702d15d4c60c60dab46de4ae01319b
