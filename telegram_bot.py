'https://api.telegram.org/'
'https://core.telegram.org/bots/api'

import requests , pathlib , os
import WebScraping_Uncuyo.Generador_de_JSON as Generador_de_JSON
from WebScraping_Uncuyo.WebScraping_PaginasUncuyo import Obteniendo_Menu_Comedor_Uncuyo

from datetime import datetime

''' # - Styles Text: MARKDOWN
- 'parse_mode':'MARKDOWN' #Necesario para que surta efecto
- *Negrita*
- _cursiva_
[inline URL](http://www.example.com/)
[inline mention of a user](tg://user?id=123456789)
`inline fixed-width code`
'''

''' # - Styles Text: HTML
- <b>bold</b>, <strong>bold</strong>
- <i>italic</i>, <em>italic</em>
- <u>underline</u>, <ins>underline</ins>
- <s>strikethrough</s>, <strike>strikethrough</strike>, <del>strikethrough</del>
- <span class="tg-spoiler">spoiler</span>, <tg-spoiler>spoiler</tg-spoiler>
- <b>bold <i>italic bold <s>italic bold strikethrough <span class="tg-spoiler">italic bold strikethrough spoiler</span></s> <u>underline italic bold</u></i> bold</b>
- <a href="http://www.example.com/">inline URL</a>
- <a href="tg://user?id=123456789">inline mention of a user</a>
- <code>inline fixed-width code</code>
- <pre>pre-formatted fixed-width code block</pre>
- <pre><code class="language-python">pre-formatted fixed-width code block written in the Python programming language</code></pre>
'''

''' # = Message
requests.post( f'https://api.telegram.org/bot{Token_bot}/sendMessage',
data = {"chat_id":'@Novedades_Uncuyo' , "text" : " *Bot* ```Diego``` ", 'parse_mode':'MARKDOWN'})
'''

'''
# - Image Photo url, 
url_imagen = "https://www.uncuyo.edu.ar/bienestar/cache/pollo-al-limon3_800_900.jpg"
text_imagen = ""
text_imagen += '<span class="tg-spoiler">spoiler</span>'
text_imagen += '<a href="https://www.uncuyo.edu.ar/bienestar/cache/pollo-al-limon3_800_900.jpg">inline URL</a>'
text_imagen += '<pre><code class="language-python">pre-formatted fixed-width code block written in the Python programming language</code></pre>'
text_imagen += '<code>inline fixed-width code</code>'
requests.post( f'https://api.telegram.org/bot{Token_bot}/sendPhoto',
	data = {"chat_id":'@Novedades_Uncuyo' ,
		"photo": url_imagen ,
		'caption': text_imagen ,
		'parse_mode':'HTML'}
	)

'''

Token_bot = '5781877065:AAGMMGMnK9rceFWm0bHvRrR0kUh1a5s0-Ug'

DIR_ACTUAL = pathlib.Path(__file__).parent.absolute() #La direccion actual
Dir_Carp_Menu_Semanal_Uncuyo = DIR_ACTUAL/"WebScraping_Uncuyo"/"Menu_Semanal_Uncuyo"

Dicc_Ultimo_Menu_Generado = Generador_de_JSON.retorna_ultima_actividad_generada( Dir_Carp_Menu_Semanal_Uncuyo )

Dicc_Menu_Semanal_Uncuyo_Comedor = Obteniendo_Menu_Comedor_Uncuyo( Dicc_Ultimo_Menu_Generado ) #Obtenemos el menu semanal

if Dicc_Menu_Semanal_Uncuyo_Comedor != {}:
	Generador_de_JSON.Generador_de_JSON_Menu_Semanal_Uncuyo( Dicc_Menu_Semanal_Uncuyo_Comedor , Dir_Carp_Menu_Semanal_Uncuyo )
	print("MENU ACTUALIZADO!!!")

	for key,list_value in Dicc_Menu_Semanal_Uncuyo_Comedor.items():
		try:
			int( key ) #Si es un numero pasara

			menu_vegetariano_y_comun = 'Menu Vegetariano'
			
			menu = list_value # 0 es normal , 1 vegetariano
			if menu[0]["Texto_Menu"] == menu[1]["Texto_Menu"]:
				menu_vegetariano_y_comun = 'Menu Vegetariano y Comun'
			else:
				text_imagen = f'<u><i><strong>{menu[0]["Fecha"]}</strong></i></u><i><strong> - Menu Comun </strong></i>\n'
				text_imagen += f'<i>{menu[0]["Texto_Menu"]}</i>\n\n'	
				
				url_imagen = menu[0]['Imagen']
				requests.post( f'https://api.telegram.org/bot{Token_bot}/sendPhoto',
					data = {"chat_id":'@Novedades_Uncuyo' ,
						"photo": url_imagen ,
						'caption': text_imagen ,
						'parse_mode':'HTML'}
					)
			
			text_imagen = f'<u><i><strong>{menu[1]["Fecha"]}</strong></i></u><i><strong> - {menu_vegetariano_y_comun} </strong></i>\n'
			text_imagen += f'<i>{menu[1]["Texto_Menu"]}</i>\n\n'
			
			url_imagen = menu[1]['Imagen']
			requests.post( f'https://api.telegram.org/bot{Token_bot}/sendPhoto',
				data = {"chat_id":'@Novedades_Uncuyo' ,
					"photo": url_imagen ,
					'caption': text_imagen ,
					'parse_mode':'HTML'}
				)
			
		except:
			pass #Es un texto fecha_generacion

else:
	print("EL MENU NO SE ACTUALIZO AUN!!!")

	now = datetime.now() #Dia actual
	menu_vegetariano_y_comun = 'Menu Vegetariano'
	
	menu = Dicc_Ultimo_Menu_Generado[ str( now.day ) ] # 0 es normal , 1 vegetariano

	# = Message
	text_Message = ""
	text_Message += f"<u><i><strong>Menu de hoy {menu[0]['Fecha']}</strong></i></u>"
	requests.post( f'https://api.telegram.org/bot{Token_bot}/sendMessage',
	data = {"chat_id":'@Novedades_Uncuyo' , "text" : f"{text_Message}", 'parse_mode':'HTML'})

	if menu[0]["Texto_Menu"] == menu[1]["Texto_Menu"]:
		menu_vegetariano_y_comun = 'Menu Vegetariano y Comun'
	else:
		text_imagen = f'<i><strong> - Menu Comun </strong></i>\n'
		text_imagen += f'<i>{menu[0]["Texto_Menu"]}</i>\n\n'	
		
		url_imagen = menu[0]['Imagen']
		requests.post( f'https://api.telegram.org/bot{Token_bot}/sendPhoto',
			data = {"chat_id":'@Novedades_Uncuyo' ,
				"photo": url_imagen ,
				'caption': text_imagen ,
				'parse_mode':'HTML'}
			)
	
	text_imagen = f'<i><strong> - {menu_vegetariano_y_comun} </strong></i>\n'
	text_imagen += f'<i>{menu[1]["Texto_Menu"]}</i>\n\n'
	
	url_imagen = menu[1]['Imagen']
	requests.post( f'https://api.telegram.org/bot{Token_bot}/sendPhoto',
		data = {"chat_id":'@Novedades_Uncuyo' ,
			"photo": url_imagen ,
			'caption': text_imagen ,
			'parse_mode':'HTML'}
		)

