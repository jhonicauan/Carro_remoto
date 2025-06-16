import websockets
import asyncio
import websockets.exceptions
from Components.Motor import Motor
from Components.Servo import Servo
import RPi.GPIO as gpio
import json

gpio.setmode(gpio.BCM)
gpio.cleanup()  

motorDireitoT = Motor(27, 22, 17)
motorEsquerdoT = Motor(10, 9, 11)
motorEsquerdoF = Motor(20, 16, 21)
motorDireitoF = Motor(7, 8, 25)
servo = Servo(19)
erro = 0

def forward(value):
    motorEsquerdoT.forward(value)
    motorDireitoT.forward(value)
    motorEsquerdoF.forward(value)
    motorDireitoF.forward(value)

def backward(value):
    motorEsquerdoT.backward(value)
    motorDireitoT.backward(value)
    motorEsquerdoF.backward(value)
    motorDireitoF.backward(value)

def right(value):
    motorEsquerdoT.forward(100)
    motorDireitoT.forward(0)
    motorEsquerdoF.forward(100)
    motorDireitoF.forward(0)

def left(value):
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

async def handler_connection(websocket, path):
    print("Conexão estabelecida")
    erro = 0  
    try:
        while True:
            try:
                message = await asyncio.wait_for(websocket.recv(), timeout=0.5)
                data = json.loads(message)
                command = data.get("command")
                value = data.get("value")
                erro = 0 
                if command == 'forward':
                    forward(value)
                    await websocket.send("motor indo para frente")
                elif command == 'backward':
                    backward(value)
                    await websocket.send("motor indo para trás")
                elif command == 'right':
                    right(value)
                    await websocket.send("virando para a direita")
                elif command == 'left':
                    left(value)
                    await websocket.send("virando para a esquerda")
                elif command == 'stop':
                    stop()
                    await websocket.send("motor parou")
                elif command == 'camera':
                    servo.set_angle(value)
                    await websocket.send("virando camera")
                elif command == 'teste':
                    await websocket.send("")
                else:
                    await websocket.send("comando não reconhecido")

            except asyncio.TimeoutError:
                erro += 1
                if erro > 2:
                    stop()

    except websockets.exceptions.ConnectionClosed:
        stop()
        print("Conexão finalizada (WebSocket)")


async def main():
    
    asyncio.create_task(monitorar_rede())

    await websockets.serve(handler_connection, "0.0.0.0", 8765)
    print("Servidor WebSocket escutando em ws://0.0.0.0:8765")
    
 
    await asyncio.Future()

asyncio.run(main())
