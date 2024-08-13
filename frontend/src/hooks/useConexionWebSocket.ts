/*
Feature a la que responde este componente:
    F6: Control de Carga Horaria Atrasada

    Como institución quiero que se notifique automáticamente el estado de la 
	carga horaria atrasada de cada docente para prevenir el incumplimiento 
	de sus respectivos horas de docencia.

Grupo encargado: Grupo 5
    - David Averos (Backend)
    - Gary Campaña (Documentación)
    - David Torres (Frontend)

Documentación asociada:
    Mapa navegacional y wireframe: https://www.figma.com/design/ihvX1EY7yVl6tCnNEyzsZQ/DCU?node-id=0-1
    Tokens de diseño: https://www.figma.com/design/ihvX1EY7yVl6tCnNEyzsZQ/DCU?node-id=116-2

Entidades backend involucradas: Docente, Aspecto, Notificacion.

Sección de la feature abordada en este componente:
    Alertas de tipo notificacion para avisar al docente el retraso del registro de su carga horaria en diferentes aspectos.
*/
/**
 * Creado por: David Torres y Gary Campaña
 */

// ConexionWebSocket.ts
import { useEffect, useState } from 'react';

// Define la estructura de una notificación recibida desde el WebSocket.
interface Notification {
    nombre_aspecto: string;        // Nombre del aspecto relacionado con la notificación.
    estado_notificacion: string;   // Estado de la notificación (por ejemplo, "bajo", "normal", "intenso", "crítico").
    notificaciones_disponibles: boolean; // Indica si hay notificaciones disponibles para este aspecto.
}

/**
 * Custom Hook para manejar la conexión a un WebSocket y gestionar notificaciones.
 * @param idDocente - Identificador del docente para el que se reciben notificaciones.
 * @returns Un objeto con las notificaciones y el conteo de notificaciones no leídas.
 */
export const useConexionWebSocket = (idDocente: number) => {
    // Estado para almacenar las notificaciones recibidas.
    const [notifications, setNotifications] = useState<Notification[]>([]);
    // Estado para almacenar el conteo de notificaciones no leídas.
    const [unreadCount, setUnreadCount] = useState<number>(0);

    useEffect(() => {
        // Establece la conexión con el WebSocket.
        const socket = new WebSocket('ws://127.0.0.1:8000/ws/notificaciones/');

        // Función que se ejecuta cuando la conexión WebSocket se establece correctamente.
        socket.onopen = () => {
            console.log('WebSocket connection established');
            // Envía el ID del docente al servidor para recibir notificaciones correspondientes.
            socket.send(JSON.stringify({ id_docente: idDocente }));
        };

        // Función que se ejecuta cuando se recibe un mensaje desde el WebSocket.
        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            console.log('Received data:', data);

            // Verifica si hay notificaciones en el mensaje recibido.
            if (data.notificaciones) {
                const filteredNotifications = data.notificaciones.filter((n: { notificaciones_disponibles: any; }) => n.notificaciones_disponibles);
                setNotifications(filteredNotifications);
                // Calcula el número de notificaciones no leídas.
        const unread = filteredNotifications.length;
        setUnreadCount(unread);
            }
        };

        // Función que se ejecuta cuando ocurre un error en la conexión WebSocket.
        socket.onerror = (error) => {
            console.error('WebSocket error:', error);
        };

        // Función que se ejecuta cuando la conexión WebSocket se cierra.
        socket.onclose = () => {
            console.log('WebSocket connection closed');
        };

        // Función de limpieza que se ejecuta cuando el componente se desmonta o el efecto se reinicia.
        return () => {
            socket.close();
        };
    }, [idDocente]); // El efecto se ejecuta cada vez que cambia el idDocente.

    // Devuelve el estado de las notificaciones y el conteo de notificaciones no leídas.
    return { notifications, unreadCount };
};

export default useConexionWebSocket;
