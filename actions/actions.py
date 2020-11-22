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
	user='rasa',
	password='rasapwd',
	host='localhost',
	database='chatbot_db',
	auth_plugin='mysql_native_password'
)
#mycursor = c.cursor(buffered=True)
mycursor = c.cursor()

class ActionVerAsignaturas(Action):
	def name(self) -> Text:
		return "action_ver_asignaturas"
		
	
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



				
