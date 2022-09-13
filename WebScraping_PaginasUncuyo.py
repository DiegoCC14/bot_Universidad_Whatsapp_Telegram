from bs4 import BeautifulSoup
import requests
import parse , pathlib , json , time

from datetime import datetime
try:
	import Generador_de_JSON
except:
	pass

def Obteniendo_Menu_Comedor_Uncuyo( Dicc_Ultimo_Menu_Encontrado ):

	Dicc_Menu_Semanal = {}
	
	page = requests.get( f"https://www.uncuyo.edu.ar/bienestar/menu" )
	soup = BeautifulSoup( page.content , "html.parser" )

	formato_fecha = parse.compile( "{dia:S} {num:d}" )

	class_content_item_menus_completo = soup.find_all( "div" , class_ = "modulo_item" ) #trae 1ro normal y luego vegetariano

	for box_div_item_menu in class_content_item_menus_completo:
		
		try:
			
			Menu_dia = box_div_item_menu.find( "p" , class_ = None ).text
			Menu_imagen = box_div_item_menu.find( "a" )["href"]
			Fecha_Menu_sin_procesar = box_div_item_menu.find( "h4" , class_ = "modulo_item_titulo").text # Titulo de la nota
			
			Fecha_Menu_procesado = formato_fecha.parse( Fecha_Menu_sin_procesar )
			'''
			print("------>>>>>>")
			print( f"Texto Menu: {Menu_dia}" )
			print(f"Fecha: {Fecha_Menu_procesado['num']} {Fecha_Menu_procesado['dia']}")
			print( f"Imagen: {Menu_imagen}" )
			print("------>>>>>>")
			'''
			if f"{Fecha_Menu_procesado['num']}" in Dicc_Ultimo_Menu_Encontrado:
				return {} #El menu de la semana pasada es el mismo que el actual, no actualizamos

			else:
				if str( Fecha_Menu_procesado['num'] ) in Dicc_Menu_Semanal:
					Dicc_Menu_Semanal[ f"{Fecha_Menu_procesado['num']}"].append( {'Texto_Menu':Menu_dia,
						'Fecha':f"{Fecha_Menu_procesado['num']} {Fecha_Menu_procesado['dia']}",
						'Imagen':Menu_imagen} )
				else:
					Dicc_Menu_Semanal[ f"{Fecha_Menu_procesado['num']}"] = [{'Texto_Menu':Menu_dia,
						'Fecha':f"{Fecha_Menu_procesado['num']} {Fecha_Menu_procesado['dia']}",
						'Imagen':Menu_imagen}]
			
		except:
			print("ERROR EN MENU UNCUYO!!")
			pass
	
	Dicc_Menu_Semanal["Fecha_Generacion"] = datetime.today().strftime('%Y-%m-%d %H:%M') 
	
	return Dicc_Menu_Semanal


if __name__ == "__main__":
		
	DIR_ACTUAL = pathlib.Path(__file__).parent.absolute() #La direccion actual

	Dir_Carp_Menu_Semanal_Uncuyo = DIR_ACTUAL/"Menu_Semanal_Uncuyo"

	Dicc_Ultimo_Menu_Generado = Generador_de_JSON.retorna_ultima_actividad_generada( Dir_Carp_Menu_Semanal_Uncuyo )
	
	Dicc_Menu_Semanal_Uncuyo_Comedor = Obteniendo_Menu_Comedor_Uncuyo( Dicc_Ultimo_Menu_Generado ) #Obtenemos el menu semanal
	if Dicc_Menu_Semanal_Uncuyo_Comedor != {}:
		Generador_de_JSON.Generador_de_JSON_Menu_Semanal_Uncuyo( Dicc_Menu_Semanal_Uncuyo_Comedor , Dir_Carp_Menu_Semanal_Uncuyo )
		print("MENU ACTUALIZADO!!!")
	else:
		print("EL MENU NO SE ACTUALIZO AUN!!!")