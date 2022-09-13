import pathlib , parse
import mysql.connector
import WebScraping_PaginasMendoza

DIR_ACTUAL = pathlib.Path(__file__).parent.absolute() #La direccion actual

class DB_Actividades_Mendoza():
	
	def __init__( self , host , password , user , port ):
		self.db_conexion = mysql.connector.connect(
			host= host,
			password= password,
			user= user,
			port= port,
			db="actividades_mendoza")	

	def cerrar_conexion( self ):
		self.db_conexion.close()

	def ver_tablas( self ):
		# sql: mysql.cursor -> Siendo mysql la conexion con DB [primero>Abrir_Conexion()]
		# -->> Retorna un lista con el nombre de todas las tablas de DB
		cur = self.db_conexion.cursor()
		cur.execute("SHOW TABLES;")
		
		Tablas = []
		for campo in cur.fetchall():
			Tablas.append(campo[0])
		return Tablas

	def ver_tabla( self , nombre_tabla ):
		# sql: mysql.cursor -> Siendo mysql la conexion con DB [primero>Abrir_Conexion()]
		# nombre_tabla: Nombre de la Tabla a ver
		# -->> Retorna una tupla con todas las filas de DB

		cur = self.db_conexion.cursor()
		Nombres_Campos_Tabla = self.ver_nombres_campos_tabla( nombre_tabla )

		cur.execute("SELECT * FROM " + nombre_tabla)
		Tabla = []
		for fila in cur.fetchall():
			Diccionario = {}
			for x in range( len( Nombres_Campos_Tabla ) ):
				Diccionario[ Nombres_Campos_Tabla[x] ] = fila[x]  
			Tabla.append( Diccionario )
		return( Tabla ) #Retorna una lista con todas las filas de DB

	def ver_nombres_campos_tabla( self , nombre_tabla ):
		#Retorna lista con los nombres de los campos de la Tabla 'nombre_tabla'
		Campos_Tabla = self.ver_campos_y_atributos_tabla( nombre_tabla )
		Nombres_Campo_Tabla = []
		for campo in Campos_Tabla:
			Nombres_Campo_Tabla.append( campo[0] )
		return Nombres_Campo_Tabla

	def ver_campos_y_atributos_tabla( self , nombre_tabla ):
		# Retorna los campos de la Tabla
		# sql: mysql.cursor -> Siendo mysql la conexion con DB [primero>Abrir_Conexion()]
		# nombre_tabla: Nombre de la Tabla a ver DESCRIPCION
		# -->> Retorna una lista con todas las filas de DB
		cur = self.db_conexion.cursor()
		cur.execute("DESCRIBE " + nombre_tabla)
		return( cur.fetchall() ) #Retorna una lista con todos los Campos de DB

	def buscar_registro_por_atributo( self , nombre_tabla , atributo , valor_buscar ):
	
		Nombres_Campos_Tabla = self.ver_nombres_campos_tabla( nombre_tabla )

		cur = self.db_conexion.cursor()
		#Consulta = "SELECT * FROM {} WHERE {} LIKE '{}' ".format( nombre_tabla , atributo , valor_buscar )
		Consulta = f"SELECT * FROM {nombre_tabla} WHERE {atributo} LIKE '{valor_buscar}' "
		cur.execute( Consulta )
		
		Tabla = []
		for fila in cur.fetchall():
			Diccionario = {}
			for x in range( len( Nombres_Campos_Tabla ) ):
				Diccionario[ Nombres_Campos_Tabla[x] ] = fila[x]
			Tabla.append( Diccionario )
		return( Tabla ) #Retorna una lista con todas las filas de DB

	def insert_registro( self , nombre_tabla , dicc_campos_registro ):
		#sql: objeto con conexion establecida en DB
		#nombre_tabla: Nombre de la tabla a Insertar
		#dicc_campos_registro: Diccionario para ingresar a la Tabla	
		cur = self.db_conexion.cursor()

		Campos_Tabla = '('
		for Campo in dicc_campos_registro.keys():
			Campos_Tabla += Campo + ','

		Campos_Tabla = Campos_Tabla[0:len(Campos_Tabla)-1] + ')'
		if( len(dicc_campos_registro.values()) == 1 ):
			Consulta = "INSERT INTO " + nombre_tabla + Campos_Tabla + " VALUES " + str( tuple(dicc_campos_registro.values()) )
			Consulta = Consulta[0:len(Consulta)-2] + ')' #Nos sale una coma al final y la sacamos
			cur.execute( Consulta )
		else:
			cur.execute("INSERT INTO " + nombre_tabla + Campos_Tabla + " VALUES " + str( tuple(dicc_campos_registro.values()) ) )
		
		self.db_conexion.commit() #Guardamos los cambios

	def insert_registro_multiples( self , nombre_tabla , dicc_campos_registro , Atributo_List_Multiple ):
		#Genera declaracion de insert de varios values.
		
		Campos_Tabla = '('
		Campo_Values = "("
		for Campo in Diccionario_Campos.keys():
			if Campo != Atributo_List_Multiple:
				Campos_Tabla += Campo + ','
				if type(Diccionario_Campos[Campo]) == str:
					Campo_Values += "'{}'".format( Diccionario_Campos[Campo] ) + "," #Tipo String
				elif type(Diccionario_Campos[Campo]) == int or type(Diccionario_Campos[Campo]) == float:
					Campo_Values += str(Diccionario_Campos[Campo]) + "," #Tipo Float
				elif type(Diccionario_Campos[Campo]) == datetime:
					Campo_Values += "TO_DATE('{}','DD/MM/YYYY')".format( Diccionario_Campos[Campo] ) + "," #Tipo Date

		Campos_Tabla += Atributo_List_Multiple #Dejamos el atributo lista al final
			
		Campos_Tabla += ')'

		Consulta = "INSERT INTO " + Nombre_Tabla + Campos_Tabla + " VALUES "
		ValuesTotal = ""
		for Atributo_list in Diccionario_Campos[Atributo_List_Multiple]:
			if type(Atributo_list) == str:
				ValuesTotal += Campo_Values + "'{}'".format( Atributo_list ) +")," #Tipo String
			elif type(Atributo_list) == int or type(Diccionario_Campos[Campo]) == float:
	 			ValuesTotal += Campo_Values + str(Atributo_list) +")," #Tipo Float
			elif type(Atributo_list) == datetime:
				ValuesTotal += Campo_Values + "TO_DATE('{}','DD/MM/YYYY')".format( Atributo_list ) +"),"

		ValuesTotal = ValuesTotal[0:len(ValuesTotal)-1]
		Consulta += ValuesTotal

		cur = sql.cursor()
		cur.execute( Consulta )
		sql.commit() #Guardamos los cambios	

	def insertar_categoria( self , dicc_campos_registro ):
		# Categorias:
			# id : PK AutoIncremental
			# nombre : varchar 
		self.insert_registro( "categorias" , dicc_campos_registro )

	def insertar_nuevo_municipio_localidad( self , dicc_campos_registro ):
		self.insert_registro( "municipalidad_o_localidad" , dicc_campos_registro )

	def ingresando_actividades_de_json( json_Actividades ):
		pass

DB_Actividades = DB_Actividades_Mendoza( 'localhost' , 'Diego42750569' , 'root' , '3306' )


Dir_Carp_Actividades_Mendoza = DIR_ACTUAL/"Actividades_Mendoza_JSON"
json_Actividades = WebScraping_PaginasMendoza.Ultimo_Json_Actividades_Generado( Dir_Carp_Actividades_Mendoza )
List_Actividades_a_cargar = WebScraping_PaginasMendoza.actividades_nuevaas_de_json( json_Actividades )


#Traemos todas las Categorias
list_registros_categoria = DB_Actividades.ver_tabla("categorias")
print( list_registros_categoria )


#Traemos todos los Liks Paginas
list_paginas_oficiales = DB_Actividades.ver_tabla("paginas_oficiales")
print( list_paginas_oficiales )


#Traemos todas las Municipalidades_Localidades
list_municipalidades_localidades = DB_Actividades.ver_tabla("municipalidad_o_localidad")
print( list_municipalidades_localidades )


formato_Municipio_Pagina = parse.compile( "{Nombre_Municipio_Localidad:S} - {Pagina:S}" )


for actividad in List_Actividades_a_cargar:

	print( "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~>>>>>>>" )
	id_Municipalidad_Localidad = None
	Municipio_Localidad = formato_Municipio_Pagina.parse( actividad['Municipalidad_Localidad'] )['Nombre_Municipio_Localidad']
	for municipalidad_localidad in list_municipalidades_localidades:
		if municipalidad_localidad["nombre"] == Municipio_Localidad
			id_Municipalidad_Localidad = municipalidad_localidad["id"]
	if id_Municipalidad_Localidad == None:
		#Ya tenemos el id_Municipalidad_Localidad
		id_Municipalidad_Localidad
		DB_Actividades.insertar_nuevo_municipio_localidad( {"nombre":Municipio_Localidad} )


	Municipalidad_Pagina = actividad['Municipalidad_Localidad']
	actividad['Link_Pagina'] #Buscamos esta url si existe

	for activ in actividad["Actividades"]:
		print("@@@@@@@@@")
		print( activ["Titulo"] )
		print( activ["Texto"] )
		print( activ["Fecha"] )
		
		if len( activ["Categorias"] ) == 0:
			if len( DB_Actividades.buscar_registro_por_atributo( 'categorias' , 'nombre' , 'Indefinido' ) ) == 0:
				print( f'INGRESANDO NUEVA CATEGORIA: Indefinido' )
		else:
			for categoria in activ["Categorias"]:
				if len( DB_Actividades.buscar_registro_por_atributo( 'categorias' , 'nombre' , categoria ) ) == 0:
					print( f'INGRESANDO NUEVA CATEGORIA: {categoria}' )
		
		print( activ["Imagen"] )
		print( activ["Link_Nota"] )
		print("@@@@@@@@@")
	
	print( "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~>>>>>>>" )



'''
DB_Actividades = DB_Actividades_Mendoza( 'localhost' , 'Diego42750569' , 'root' , '3306' )
#print( DB_Actividades.ver_tablas() )


print( DB_Actividades.ver_tabla( 'actividades' ) )

print( DB_Actividades.ver_nombres_campos_tabla( 'actividades' ) )

print( DB_Actividades.ver_nombres_campos_tabla( 'categorias' ) )

print( DB_Actividades.ver_tabla( 'categorias' ) )

#DB_Actividades.insert_registro( 'categorias' , {"nombre":"Arbolado"} )
#DB_Actividades.insert_registro( 'categorias' , {"nombre":"Deportes"} )

DB_Actividades.cerrar_conexion()
'''