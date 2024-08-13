import React, { useRef, useState } from 'react';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import Perfil from '../assets/perfil.svg';
import { useContextoGlobal } from '../ContextoGlobal';
import { BiBell, BiError, BiSolidMessageError, BiCheckCircle } from 'react-icons/bi';
import useConexionWebSocket from '../hooks/useConexionWebSocket'; // Asegúrate de que la ruta sea correcta
import { Modal, Button, ProgressBar, Table } from 'react-bootstrap'; // Asegúrate de tener react-bootstrap importado

import 'bootstrap/dist/css/bootstrap.min.css';
import '../styles/components/BarraNavegacion.css';

function BarraNavegacion() {
    const { paginaActual, setPaginaActual, setRol, setAsignatura, setCurso, setUsuario, rol } = useContextoGlobal();
    const notificacionesRef = useRef<any>(null);
    const [mostrarNotificaciones, setMostrarNotificaciones] = useState(false);
    const { notifications, unreadCount } = useConexionWebSocket(1); // Aquí pasas el id_docente

    // Estado para el modal
    const [modalShow, setModalShow] = useState(false);
    const [notificacionSeleccionada, setNotificacionSeleccionada] = useState<any>(null);

    const cambiarPagina = (pagina: string) => {
        setPaginaActual(pagina);
    };

    const cerrarSesion = () => {
        setRol('');
        setUsuario('');
        setAsignatura(0);
        setCurso(0);
        setPaginaActual('Login');
    };

    const handleBellClick = () => {
        setMostrarNotificaciones(prevState => !prevState);
        if (notificacionesRef.current) {
            notificacionesRef.current.recargarNotificaciones();
        }
    };

/**
 * Modificado por: David Torres y Gary Campaña
 */
    const handleNotificationClick = (notification: any) => {
        setNotificacionSeleccionada(notification);
        setModalShow(true);
    };

    const handleCloseModal = () => {
        setModalShow(false);
        setNotificacionSeleccionada(null);
    };

    // Función para obtener el ícono basado en el estado de la notificación
    const getNotificationIcon = (estado: string) => {
        switch (estado) {
            case 'CRITICO':
                return <BiError color="red" />;
            case 'INTENSO':
                return <BiSolidMessageError color="orange" />;
            case 'NORMAL':
            case 'BAJO':
                return <BiCheckCircle color="blue" />;
            default:
                return <BiBell />;
        }
    };

    const getProgressBarColor = (estado: string) => {
        switch (estado) {
            case 'CRITICO':
                return 'red';
            case 'INTENSO':
                return 'orange';
            case 'NORMAL':
            case 'BAJO':
                return 'lightblue';
            default:
                return 'gray';
        }
    };

    return (
        <>
            <Navbar className="nav-bar" data-bs-theme="dark">
                <Navbar.Brand>SYNCADEMIC</Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse className="justify-content-end">
                    <Nav>
                        <img src={Perfil} width={15} alt="Perfil" />
                        <NavDropdown title={`Perfil ${rol}`} data-bs-theme="light">
                            <NavDropdown.Header>Perfil del {rol}</NavDropdown.Header>
                            {rol === 'docente' && (
                                <>
                                    <NavDropdown.Item onClick={() => cambiarPagina('Cursos')}>Cursos</NavDropdown.Item>
                                    <NavDropdown.Item onClick={() => cambiarPagina('Capacitaciones')}>Capacitaciones</NavDropdown.Item>
                                </>
                            )}
                            <NavDropdown.Divider />
                            <NavDropdown.Item onClick={() => cerrarSesion()}>Cerrar sesión</NavDropdown.Item>
                        </NavDropdown>
                        {paginaActual === 'Home' && (
                            <NavDropdown
                                title={<><BiBell size={24} /> {unreadCount > 0 && <span className="notification-icon">{unreadCount}</span>}</>}
                                id="notifications-dropdown"
                                show={mostrarNotificaciones}
                                onClick={handleBellClick}
                                align="end"
                                className="notifications-dropdown"
                            >
                                <NavDropdown.Item className='notification-item2' style={{ color: 'black' }}><h4 className="no-hover">Notificaciones</h4><h6 style={{ color: 'white' }}>Atrasado en:</h6></NavDropdown.Item>

                                {notifications.length > 0 ? (
                                    notifications.map((notification, index) => (
                                        <NavDropdown.Item
                                            key={index}
                                            onClick={() => handleNotificationClick(notification)}
                                            className="notification-item"
                                        >
                                            <div className="notification-content">
                                                <span className="notification-icon2">{getNotificationIcon(notification.estado_notificacion)}</span>
                                                <h6 className="notification-aspecto">{notification.nombre_aspecto}</h6>
                                                <span className="notification-vermas">ver más</span>
                                            </div>
                                        </NavDropdown.Item>
                                    ))
                                ) : (
                                    <NavDropdown.Item disabled>No hay notificaciones</NavDropdown.Item>
                                )}
                            </NavDropdown>
                        )}
                    </Nav>
                </Navbar.Collapse>
            </Navbar>

            {/* Modal para mostrar detalles de la notificación */}
            {notificacionSeleccionada && (
                <Modal show={modalShow} onHide={handleCloseModal} centered >
                    <Modal.Header closeButton style={{backgroundColor: '#DADADA'}}>
                        <Modal.Title>{getNotificationIcon(notificacionSeleccionada.estado_notificacion)} Detalles de la notificación</Modal.Title> {/* Ícono en el título */}
                    </Modal.Header>
                    <Modal.Body>
                        <h5><strong>Retraso de horas registradas en: </strong> {notificacionSeleccionada.mensaje.nombre_aspecto}</h5>
                        <p><strong>Fecha final para registrar: </strong> {notificacionSeleccionada.mensaje.fecha_fin}</p>
                        <p><strong>Progreso de registro actual: </strong></p>
                        <ProgressBar
                            now={notificacionSeleccionada.mensaje.progreso_general_porcentaje}
                            variant="custom"
                            className="progress-bar-custom"
                            style={{ backgroundColor: '#DADADA', fontWeight: 'bold' ,height: '30px', color: 'black'}}
                        >
                            <ProgressBar
                                now={notificacionSeleccionada.mensaje.progreso_general_porcentaje}
                                style={{ backgroundColor: getProgressBarColor(notificacionSeleccionada.estado_notificacion), color: 'white' }}
                                label={`${notificacionSeleccionada.mensaje.progreso_general_porcentaje}%`}
                            />
                        </ProgressBar>
                        <Table striped bordered hover>
                            <thead>
                                <tr>
                                    <th>Áreas</th>
                                    <th>Progreso</th>
                                </tr>
                            </thead>
                            <tbody>
                                {notificacionSeleccionada.mensaje.subaspectos && notificacionSeleccionada.mensaje.subaspectos.map((subaspecto: any, index: number) => (
                                    <tr key={index}>
                                        <td>{subaspecto.nombre}</td>
                                        <td>
                                            <ProgressBar
                                                now={subaspecto.progreso}
                                                variant="custom"
                                                style={{ backgroundColor: '#DADADA', height: '20px' }}
                                            >
                                                <ProgressBar
                                                    now={subaspecto.progreso}
                                                    style={{ backgroundColor: getProgressBarColor(notificacionSeleccionada.estado_notificacion) }}
                                                    label={`${subaspecto.progreso}%`}
                                                />
                                            </ProgressBar>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </Table>
                    </Modal.Body>
                    <Modal.Footer>
                        <Button variant="danger" onClick={handleCloseModal}>
                            Cerrar
                        </Button>
                    </Modal.Footer>
                </Modal>
            )}
        </>
    );
}

export default BarraNavegacion;