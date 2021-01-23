import re
import pprint

# 1) Lectura ficheros
tema1 = open("preguntes-VC2020-Tema 1 - Formació (entrenament)-20201001-1947.txt", "r", encoding='utf-8')
tema2 = open("preguntes-VC2020-Tema 2 - Processament (entrenament)-20201001-1951.txt", "r", encoding='utf-8')

# 2) Función parseado
def parser(tema):
    pregunta = {}
    preguntas = []
    for line in tema:
        if line != '' and line[:1] != '}' and line != '\n':
            
            # datos pregunta
            if line[:2] == "//":
                # inicializar contenedores   
                aux = []
                opciones = []
                pregunta = {}
                pregunta['respuestas'] = []

                # procesar datos - lista
                aux = line.split('// ')
                datos = aux[1].split('\n')
                pregunta['datos'] = datos[0]
                aux = datos[0].split(' ')
                pregunta['numero'] = aux[1]


            # enunciado
            elif line[:2] == '::':
                aux = []
                aux = line.split('<p>')
                enunciado = aux[1].split('<br>')
                pregunta['enunciado'] = enunciado[0]

            # respuestas
            else:
                aux = []
                aux = line.split('<p>')
                if aux[0].strip() == '=':
                    opcionCorrecta = True
                else:
                    opcionCorrecta = False
                respuesta = aux[1].split('<br>')
                pregunta['respuestas'].append([opcionCorrecta, respuesta[0]])

                if len(pregunta['respuestas']) == 4:
                    preguntas.append(pregunta)

    # for pregunta in preguntas:
    #     print(pregunta['numero'])
    #     print(pregunta['datos'])
    #     print(pregunta['enunciado'])
    #     print(pregunta['respuestas'])
    #     print(pregunta['respuestas'][0])
    #     print(pregunta['respuestas'][0][0])
     
    return preguntas

# 3) Guardar preguntas
preguntasT1 = parser(tema1)
preguntasT2 = parser(tema2)

# 4) Conectar a BD
import pymongo
client = pymongo.MongoClient("localhost", 27017)
mongodb = client["preguntas"]
collection = mongodb["102784"]

# 5) Insertar preguntas en colecciones

#  "tema": "",
#  "numPregunta": "",
#  "enunciado": "",
#     "opciones": [
#         {
#             "option1": "1",
#             "isCorrect": false
#         },
#         {
#             "option2": "2",
#             "isCorrect": true
#         },
#         {
#             "option3": "3",
#             "isCorrect": false
#         },
#         {
#             "option3": "3",
#             "isCorrect": false
#         }
#     ]

# Insert Tema 1
for pregunta in preguntasT1:
    
    p = {   "tema":"1", "numPregunta": pregunta['numero'], "enunciado": pregunta['enunciado'],
            "opciones":[
                {   "isCorrect": pregunta['respuestas'][0][0],
                    "opcion1": pregunta['respuestas'][0][1]},
                {   "isCorrect": pregunta['respuestas'][1][0],
                    "opcion2": pregunta['respuestas'][1][1]},
                {   "isCorrect": pregunta['respuestas'][2][0],
                    "opcion3": pregunta['respuestas'][2][1]},
                {   "isCorrect": pregunta['respuestas'][3][0],
                    "opcion4": pregunta['respuestas'][3][1]},
            ]}

    collection.insert_one(p)

# Insert Tema 2
for pregunta in preguntasT2:
    
    p = {   "tema":"2", "numPregunta": pregunta['numero'], "enunciado": pregunta['enunciado'],
            "opciones":[
                {   "isCorrect": pregunta['respuestas'][0][0],
                    "opcion1": pregunta['respuestas'][0][1]},
                {   "isCorrect": pregunta['respuestas'][1][0],
                    "opcion2": pregunta['respuestas'][1][1]},
                {   "isCorrect": pregunta['respuestas'][2][0],
                    "opcion3": pregunta['respuestas'][2][1]},
                {   "isCorrect": pregunta['respuestas'][3][0],
                    "opcion4": pregunta['respuestas'][3][1]},
            ]}

    collection.insert_one(p)


# # 6) Generar preguntas al azar

# # Una pregunta al azar
# x = collection.aggregate([{ "$sample": { "size": 1 } }])
# # Una pregunta al azar de un tema concreto
# # x = collection.aggregate([ { "$match": { "tema": "2" }}, {"$sample": { "size": 1 } }])

# pprint.pprint(list(x))