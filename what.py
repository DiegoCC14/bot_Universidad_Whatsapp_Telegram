import pyautogui as pg, webbrowser as webSite, time

# https://www.youtube.com/watch?v=mVfm74YHEVQ
'''
numero_telefono = "+5492615055266"
pywhatkit.sendwhatmsg(numero_telefono , "Test" , 0 , 2)
'''

webSite.open( 'https://web.whatsapp.com/send?phone=+5492615055266&text=HOLA DIEGO ESTO ES UNA BROMA PA YOUTUBE' )

time.sleep(10)

pg.write("HOLA DIEGO BUENAS")
pg.press("enter")