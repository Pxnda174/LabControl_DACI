import network
import socket
from machine import Pin

led = Pin(8, Pin.OUT)

def leer_html(archivo):
    """Lee el archivo HTML almacenado en el sistema de archivos."""
    with open(archivo, 'r') as f:
        return f.read()

def conectar_wifi(ssid, password):
    """Conecta la ESP32 a una red Wi-Fi existente."""
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    sta.connect(ssid, password)
    
    print("Conectando al Wi-Fi...")
    for _ in range(20):  # Espera hasta 10 segundos
        if sta.isconnected():
            print(f"Conectado a {ssid}")
            print(f"Dirección IP: {sta.ifconfig()}")
            return sta.ifconfig()[0]
        utime.sleep(0.5)
    print("No se pudo conectar al Wi-Fi.")
    return None

# Configuración de red Wi-Fi
WIFI_SSID = "TP-Link_B970"
WIFI_PASSWORD = "12345679"

# Conectar al Wi-Fi
ip_local = conectar_wifi(WIFI_SSID, WIFI_PASSWORD)

if ip_local:
    # Configurar el servidor web
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    servidor = socket.socket()
    servidor.bind(addr)
    servidor.listen(1)
    
    print(f"Servidor web iniciado en http://{ip_local}:80")
    
    while True:
        cliente, direccion = servidor.accept()
        print('Cliente conectado desde:', direccion)
        
        # Lee la solicitud del cliente
        request = cliente.recv(1024).decode('utf-8')
        request_line = request.split('\n')[0]
        path = request_line.split(' ')[1]
        print("Solicitud:", request_line)
        
        # Manejar encendido/apagado del LED
        if path == '/open?':
            led.on()
        elif path == '/close?':
            led.off()
        
        # Respuesta al cliente
        pagina_html = leer_html('index.html')
        response = f"""\
HTTP/1.1 200 OK

{pagina_html}
"""
        cliente.send(response)
        cliente.close()
else:
    print("Abortando: no hay conexión Wi-Fi.")
