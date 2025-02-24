import socket
import threading

class Computer:
    def __init__(self, name, processors, free_ram, free_disk, temperature=None):
        self.name = name
        self.processors = processors
        self.free_ram = free_ram
        self.free_disk = free_disk
        self.temperature = temperature

class Server:
    def __init__(self, host='0.0.0.0', port=5000):
        self.host = host
        self.port = port
        self.computers = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Servidor escutando em {self.host}:{self.port}")

    def handle_client(self, client_socket):
        data = client_socket.recv(1024).decode('utf-8')
        name, processors, free_ram, free_disk, temperature = data.split(',')

        if temperature.strip():  
            temperature = float(temperature)
        else:
            temperature = None  

        computer = Computer(name, int(processors), float(free_ram), float(free_disk), temperature)
        self.computers.append(computer)
        print(f"Computador {name} adicionado.")
        client_socket.close()

    def calculate_average(self):
        if not self.computers:
            return None

        avg_processors = sum(c.processors for c in self.computers) / len(self.computers)
        avg_ram = sum(c.free_ram for c in self.computers) / len(self.computers)
        avg_disk = sum(c.free_disk for c in self.computers) / len(self.computers)

        # Calcula a média de temperatura apenas se estiver disponível
        temps = [c.temperature for c in self.computers if c.temperature is not None]
        avg_temp = sum(temps) / len(temps) if temps else None

        return avg_processors, avg_ram, avg_disk, avg_temp

    def list_computers(self):
        if not self.computers:
            print("Nenhum computador conectado.")
            return

        print("\nLista de computadores conectados:")
        for i, computer in enumerate(self.computers):
            print(f"{i + 1}. {computer.name}")

    def detail_computer(self, index):
        if 0 <= index < len(self.computers):
            computer = self.computers[index]
            print(f"\nDetalhes do computador {computer.name}:")
            print(f"  Processadores: {computer.processors}")
            print(f"  Memória RAM livre: {computer.free_ram:.2f} GB")
            print(f"  Espaço em disco livre: {computer.free_disk:.2f} GB")
            if computer.temperature is not None:
                print(f"  Temperatura: {computer.temperature:.2f} °C")
            else:
                print("  Temperatura: Não disponível")
        else:
            print("Índice inválido.")

    def show_average(self):
        if not self.computers:
            print("Nenhum computador conectado.")
            return

        avg_processors, avg_ram, avg_disk, avg_temp = self.calculate_average()
        print("\nMédia dos dados dos computadores:")
        print(f"  Processadores: {avg_processors:.2f}")
        print(f"  Memória RAM livre: {avg_ram:.2f} GB")
        print(f"  Espaço em disco livre: {avg_disk:.2f} GB")
        if avg_temp is not None:
            print(f"  Temperatura: {avg_temp:.2f} °C")
        else:
            print("  Temperatura: Não disponível")

    def start(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Conexão recebida de {addr}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def menu(self):
        while True:
            print("\n--- Menu do Servidor ---")
            print("1. Listar computadores conectados")
            print("2. Detalhar um computador")
            print("3. Mostrar média dos dados")
            print("4. Sair")
            choice = input("Escolha uma opção: ")

            if choice == '1':
                self.list_computers()
            elif choice == '2':
                index = int(input("Digite o número do computador: ")) - 1
                self.detail_computer(index)
            elif choice == '3':
                self.show_average()
            elif choice == '4':
                print("Encerrando o servidor...")
                break
            else:
                print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    server = Server()

    server_thread = threading.Thread(target=server.start)
    server_thread.start()

    server.menu()