import websockets
import asyncio
import websockets.exceptions
from Components.Motor import Motor
import RPi.GPIO as gpio


gpio.setmode(gpio.BCM)
gpio.cleanup()  

motorEsquerdoT = Motor(22, 27, 17)
motorDireitoT = Motor(10, 9, 11)
motorEsquerdoF = Motor(20, 16, 21)
motorDireitoF = Motor(8, 7, 25)


def forward():
    motorEsquerdoT.forward(100)
    motorDireitoT.forward(100)
    motorEsquerdoF.forward(100)
    motorDireitoF.forward(100)

def backward():
    motorEsquerdoT.backward(100)
    motorDireitoT.backward(100)
    motorEsquerdoF.backward(100)
    motorDireitoF.backward(100)

def left():
    motorEsquerdoT.forward(100)
    motorDireitoT.forward(0)
    motorEsquerdoF.forward(100)
    motorDireitoF.forward(0)

def right():
    motorEsquerdoT.forward(0)
    motorDireitoT.forward(100)
    motorEsquerdoF.forward(0)
    motorDireitoF.forward(100)

def stop():
    motorDireitoT.stop()
    motorEsquerdoT.stop()
    motorEsquerdoF.stop()
    motorDireitoF.stop()
    print("Motor parado (stop chamado)")


def is_network_online():
    interface = "wlan0"  
    try:
        with open(f"/sys/class/net/{interface}/operstate") as f:
            return f.read().strip() == "up"
    except FileNotFoundError:
        return False


async def monitorar_rede():
    while True:
        if not is_network_online():
            print("Conexão de rede perdida. Parando o motor.")
            stop()
        await asyncio.sleep(0.5)

# WebSocket handler
async def handler_connection(websocket, path):
    print("Conexão estabelecida")
    try:
        async for message in websocket:
            if message == 'forward':
                forward()
                await websocket.send("motor indo para frente")
            elif message == 'backward':
                backward()
                await websocket.send("motor indo para trás")
            elif message == 'right':
                right()
                await websocket.send("virando para a direita")
            elif message == 'left':
                left()
                await websocket.send("virando para a esquerda")
            elif message == 'stop':
                stop()
                await websocket.send("motor parou")
            elif message == 'teste':
                await websocket.send("")
            else:
                await websocket.send("comando não reconhecido")
    except websockets.exceptions.ConnectionClosed:
        stop()
        print("Conexão finalizada (WebSocket)")


async def main():
    
    asyncio.create_task(monitorar_rede())

    await websockets.serve(handler_connection, "0.0.0.0", 8765)
    print("Servidor WebSocket escutando em ws://0.0.0.0:8765")
    
 
    await asyncio.Future()

# Executa a aplica��o
asyncio.run(main())
