import socket
import psutil
import platform

def get_system_info():
    name = platform.node()
    processors = psutil.cpu_count(logical=True)
    free_ram = psutil.virtual_memory().available / (1024 ** 3) 
    free_disk = psutil.disk_usage('/').free / (1024 ** 3)  

    if platform.system() == "Windows":
        temperature = "" 
    else:
        try:
            temperature = psutil.sensors_temperatures().get('coretemp', [{}])[0].get('current', None)
            if temperature is None:
                temperature = ""  
        except Exception as e:
            print(f"Erro ao obter temperatura: {e}")
            temperature = ""

    return name, processors, free_ram, free_disk, temperature

def send_data_to_server(server_ip, server_port):
    name, processors, free_ram, free_disk, temperature = get_system_info()
    data = f"{name},{processors},{free_ram},{free_disk},{temperature}"
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    client_socket.send(data.encode('utf-8'))
    client_socket.close()

if __name__ == "__main__":
    send_data_to_server('127.0.0.1', 5000)