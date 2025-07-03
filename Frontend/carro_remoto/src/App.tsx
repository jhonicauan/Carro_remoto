// (importações permanecem iguais)
import { useEffect, useState, useRef } from "react";
import './App.css';

import cameraIcon from "./img/cameraIcon.png";
import carIcon from "./img/carIcon.png";
import controllerIcon from "./img/controllericon.png";
import stopImg from "./img/1.png";
import forwardImg from "./img/2.png";
import backwardImg from "./img/3.png";
import rightImg from "./img/4.png";
import leftImg from "./img/5.png";
import loading from "./img/waiting.png";

type Command = "forward" | "backward" | "left" | "right" | "stop" | "camera";
type CarImage = string;

function App() {
  const [carDirection, setCarDirection] = useState<CarImage>(stopImg);
  const [controller, setController] = useState<"teclado" | "gamepad">("teclado");
  const [isMobile, setIsMobile] = useState(false);
  const [cameraPosition, setCameraPosition] = useState(90);
  const [isLoading, setIsLoading] = useState(true);
  const [cameraSrc, setCameraSrc] = useState("http://100.97.209.54:8000/stream");

  const socketRef = useRef<WebSocket | null>(null);
  const keyIntervalRef = useRef<number | null>(null);
  const touchIntervalRef = useRef<number | null>(null);
  const cameraPositionRef = useRef<number>(cameraPosition);
  const retryIntervalRef = useRef<number | null>(null);
  const reconnectTimeoutRef = useRef<number | null>(null);

  useEffect(() => {
    cameraPositionRef.current = cameraPosition;
  }, [cameraPosition]);

  const checkMobile = () => setIsMobile(window.innerWidth <= 768);

  const toggleController = () => {
    setController(prev => (prev === "teclado" ? "gamepad" : "teclado"));
  };

  const sendCommand = (command: Command, value: number) => {
    if (socketRef.current?.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify({ command, value }));
    }
  };

  // WebSocket com reconexão automática
  const connectWebSocket = () => {
    if (socketRef.current?.readyState === WebSocket.OPEN) return;

    const socket = new WebSocket("ws://100.97.209.54:8765");
    socketRef.current = socket;

    socket.onopen = () => {
      console.log("Conectado ao servidor WebSocket");
      sendCommand("stop", 0);
    };

    socket.onmessage = (event) => {
      console.log("Servidor:", event.data);
    };

    socket.onerror = () => {
      console.warn("Erro na conexão WebSocket");
    };

    socket.onclose = () => {
      console.warn("WebSocket desconectado. Tentando reconectar em 5s...");
      reconnectTimeoutRef.current = window.setTimeout(connectWebSocket, 5000);
    };
  };

  useEffect(() => {
    checkMobile();
    window.addEventListener("resize", checkMobile);

    connectWebSocket();

    const gamepadInterval = setInterval(() => {
      const gp = navigator.getGamepads()[0];
      if (!gp || controller !== "gamepad" || isMobile) return;

      const [x] = gp.axes;
      const RT = gp.buttons[7]?.value || 0;
      const LT = gp.buttons[6]?.value || 0;

      if (x > 0.2) {
        sendCommand("right", 100);
        setCarDirection(rightImg);
      } else if (x < -0.2) {
        sendCommand("left", 100);
        setCarDirection(leftImg);
      } else if (LT > 0.2) {
        sendCommand("backward", LT * 100);
        setCarDirection(backwardImg);
      } else if (RT > 0.2) {
        sendCommand("forward", RT * 100);
        setCarDirection(forwardImg);
      } else {
        sendCommand("stop", 0);
        setCarDirection(stopImg);
      }
    }, 100);

    const cameraInterval = setInterval(() => {
      const gp = navigator.getGamepads()[0];
      if (!gp || controller !== "gamepad" || isMobile) return;

      const cameraX = Number(gp.axes[2].toFixed(2)) * 100;
      let cameraValue = Math.round(90 + (cameraX * 0.9) * -1);
      if (cameraValue > 140) cameraValue = 140;
      if (cameraValue < 40) cameraValue = 40;

      if (Math.round(cameraPositionRef.current) === cameraValue) return;

      setCameraPosition(cameraValue);
      cameraPositionRef.current = cameraValue;
      sendCommand("camera", cameraValue);
    }, 100);

    const handleKeyDown = (event: KeyboardEvent) => {
      if (isMobile || controller !== "teclado" || keyIntervalRef.current) return;

      let command: Command | null = null;
      let image: CarImage | null = null;

      switch (event.key) {
        case "ArrowUp": command = "forward"; image = forwardImg; break;
        case "ArrowDown": command = "backward"; image = backwardImg; break;
        case "ArrowLeft": command = "left"; image = leftImg; break;
        case "ArrowRight": command = "right"; image = rightImg; break;
      }

      if (command && image) {
        sendCommand(command, 100);
        setCarDirection(image);

        keyIntervalRef.current = window.setInterval(() => {
          sendCommand(command!, 100);
          setCarDirection(image!);
        }, 100);
      }
    };

    const handleKeyUp = () => {
      if (keyIntervalRef.current) {
        clearInterval(keyIntervalRef.current);
        keyIntervalRef.current = null;
      }
      sendCommand("stop", 0);
      setCarDirection(stopImg);
    };

    window.addEventListener("keydown", handleKeyDown);
    window.addEventListener("keyup", handleKeyUp);

    return () => {
      window.removeEventListener("resize", checkMobile);
      window.removeEventListener("keydown", handleKeyDown);
      window.removeEventListener("keyup", handleKeyUp);
      clearInterval(gamepadInterval);
      clearInterval(cameraInterval);
      if (retryIntervalRef.current) clearInterval(retryIntervalRef.current);
      if (reconnectTimeoutRef.current) clearTimeout(reconnectTimeoutRef.current);
      socketRef.current?.close();
    };
  }, [controller, isMobile]);

  const handleTouchStart = (command: Command, image: CarImage) => {
    if (touchIntervalRef.current) return;

    sendCommand(command, 100);
    setCarDirection(image);

    touchIntervalRef.current = window.setInterval(() => {
      sendCommand(command, 100);
      setCarDirection(image);
    }, 100);
  };

  const handleTouchEnd = () => {
    if (touchIntervalRef.current) {
      clearInterval(touchIntervalRef.current);
      touchIntervalRef.current = null;
    }
    sendCommand("stop", 0);
    setCarDirection(stopImg);
  };

  const tryReloadCamera = () => {
    const newSrc = `http://100.97.209.54:8000/stream?t=${Date.now()}`;
    setCameraSrc(newSrc);
  };

  const handleCameraLoad = () => {
    setIsLoading(false);
    if (retryIntervalRef.current) {
      clearInterval(retryIntervalRef.current);
      retryIntervalRef.current = null;
    }
  };

  const handleCameraError = () => {
    setIsLoading(true);
    if (!retryIntervalRef.current) {
      retryIntervalRef.current = window.setInterval(() => {
        tryReloadCamera();
      }, 5000);
    }
  };

  return (
    <div className="divprincipal">
      <div className="camera">
        <div className="info">
          <h1>Camera do carro</h1>
          <img src={cameraIcon} alt="camera" />
        </div>
        <div className="view camera-view">
          {isLoading && (
            <div className="loading-overlay">
              <img src={loading} alt="Carregando..." className="loading-img" />
            </div>
          )}
          <img
            src={cameraSrc}
            alt="stream"
            onLoad={handleCameraLoad}
            onError={handleCameraError}
            className={isLoading ? "hidden" : ""}
          />
        </div>
      </div>

      {!isMobile && (
        <div className="car">
          <div className="info">
            <h1>Direção do carro</h1> 
            <img src={carIcon} alt="carro" /> 
          </div>
           <div className="view"> 
            <img src={carDirection} alt="direção do carro" />
          </div> 
        </div> )}
          <div className="carcontrols">
    <div className="info">
      <h1>Controles</h1>
      <img src={controllerIcon} alt="controle" />
    </div>
    <div className={`controls ${isMobile ? "mobile-controls" : ""}`}>
      {isMobile ? (
        <div className="mobile-buttons">
          <div className="row">
            <button onPointerDown={() => handleTouchStart("forward", forwardImg)} onPointerUp={handleTouchEnd}>↑</button>
          </div>
          <div className="row">
            <button onPointerDown={() => handleTouchStart("left", leftImg)} onPointerUp={handleTouchEnd}>←</button>
            <button onPointerDown={() => handleTouchStart("backward", backwardImg)} onPointerUp={handleTouchEnd}>↓</button>
            <button onPointerDown={() => handleTouchStart("right", rightImg)} onPointerUp={handleTouchEnd}>→</button>
          </div>
        </div>
      ) : (
        <button onClick={toggleController}>{controller}</button>
      )}
    </div>
  </div>
</div>);}

export default App;
