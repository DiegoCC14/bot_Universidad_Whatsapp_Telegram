import pathlib , os
import re , parse , json


DIR_ACTUAL = pathlib.Path(__file__).parent.absolute() #La direccion actual

def Generador_de_JSON_Menu_Semanal_Uncuyo( Dicc_Menu_Semanal , Dir_Carp_Salida ):
	ult_numero = archivo_JSON_con_numero_mas_alto( Dir_Carp_Salida )
	with open(Dir_Carp_Salida/f'{ult_numero+1}.json', 'w' , encoding='utf-8') as file:
		json.dump( Dicc_Menu_Semanal , file, indent=2 , ensure_ascii= False ) #utf8

def Generador_de_JSON_Actividades_Mendoza( List_Actividades , Dir_Carp_Salida ):
	
	num_mas_grande = archivo_JSON_con_numero_mas_alto( Dir_Carp_Salida )
	with open(DIR_ACTUAL/f'Actividades_Mendoza_JSON/{num_mas_grande+1}.json', 'w' , encoding='utf-8') as file:
		json.dump( List_Actividades , file, indent=2 , ensure_ascii= False ) #utf8


def archivo_JSON_con_numero_mas_alto( dir_carpeta ):

	Formato_file_json = parse.compile( "{nombre_file:d}.json" or "{nombre_file:d}.JSON" )
	
	num_maximo = 0
	for fichero in os.listdir(dir_carpeta) :
		if os.path.isfile( os.path.join(dir_carpeta, fichero) ) and ( fichero.endswith('.json') or fichero.endswith('.JSON') ) :
			resultado_1 = Formato_file_json.parse( fichero )
			if resultado_1 != None:
				num_file = int( resultado_1['nombre_file'] )
				if num_file>num_maximo:
					num_maximo = num_file
	return num_maximo

def leer_archivo_json( dir_file_json ):
	with open( dir_file_json , encoding='utf-8') as json_file:
		data = json.load(json_file)
		#data_dumps = json.dumps( data , indent=2) #Solo sirve para mostrar ordenadamente los datos
	return data

def retorna_ultima_actividad_generada( Dir_Carp_Actividades_Mendoza ):
	num_json = archivo_JSON_con_numero_mas_alto( Dir_Carp_Actividades_Mendoza )
	ultimo_json = leer_archivo_json( Dir_Carp_Actividades_Mendoza/f"{num_json}.json" )
	return ultimo_json

if __name__ == '__main__':
	Dir_Carp_Actividades_Mendoza = DIR_ACTUAL/"Menu_Semanal_Uncuyo"
	json_file = retorna_ultima_actividad_generada( Dir_Carp_Actividades_Mendoza )
	print( json_file )
	