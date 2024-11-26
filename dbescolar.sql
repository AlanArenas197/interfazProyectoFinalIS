-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 26-11-2024 a las 05:16:38
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `dbescolar`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alumnos`
--

CREATE TABLE `alumnos` (
  `alumnos_id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `apaterno` varchar(70) NOT NULL,
  `amaterno` varchar(70) NOT NULL,
  `email` varchar(256) NOT NULL,
  `estado` varchar(20) NOT NULL,
  `fecha_nac` varchar(20) NOT NULL,
  `carrera` varchar(70) NOT NULL,
  `materia` varchar(500) NOT NULL,
  `password` varchar(128) NOT NULL,
  `grupo` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `alumnos`
--

INSERT INTO `alumnos` (`alumnos_id`, `nombre`, `apaterno`, `amaterno`, `email`, `estado`, `fecha_nac`, `carrera`, `materia`, `password`, `grupo`) VALUES
(1, 'Jared', 'Castillo', 'Blanco', 'jaredmotorola@gmail.com', 'Nuevo León', '20/10/2005', 'Ingeniería en Computación', 'Programación para Internet, Base de Datos', 'jared123', 'UnoDos'),
(2, 'Francisco', 'Sanchez', 'Rodriguez', 'pacosanchezoficialyt@gmail.com', 'Jalisco', '15/07/2003', 'Ingeniería en Computación', 'Programación para Internet, Base de Datos', 'Depeche124', 'UnoDos'),
(3, 'Alan', 'Arenas', 'Venegas', 'hola@gmail.com', 'Baja California', '12/6/2001', 'Ingeniería en Computación', 'Base de Datos', '123334', 'UnoDos');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `carreras`
--

CREATE TABLE `carreras` (
  `carrera_id` int(11) NOT NULL,
  `nombre` varchar(120) NOT NULL,
  `num_semestres` int(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `carreras`
--

INSERT INTO `carreras` (`carrera_id`, `nombre`, `num_semestres`) VALUES
(1, 'Ingeniería en Computación', 9),
(2, 'Ingeniería en Sistemas', 8);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `grupos`
--

CREATE TABLE `grupos` (
  `grupo_id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `fecha` varchar(70) NOT NULL,
  `carrera` varchar(70) NOT NULL,
  `materia` varchar(500) NOT NULL,
  `maestro` varchar(150) NOT NULL,
  `salon` varchar(50) NOT NULL,
  `horario` varchar(70) NOT NULL,
  `semestre` varchar(10) NOT NULL,
  `max_alumnos` int(10) NOT NULL,
  `alum_reg` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `grupos`
--

INSERT INTO `grupos` (`grupo_id`, `nombre`, `fecha`, `carrera`, `materia`, `maestro`, `salon`, `horario`, `semestre`, `max_alumnos`, `alum_reg`) VALUES
(1, 'UnoDos', '19/11/2024', 'Ingeniería en Computación', 'Base de Datos', 'Juan', 'X10', '7:00-9:00', '2024B', 3, 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `horarios`
--

CREATE TABLE `horarios` (
  `horario_id` int(11) NOT NULL,
  `turno` varchar(50) NOT NULL,
  `hora` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `horarios`
--

INSERT INTO `horarios` (`horario_id`, `turno`, `hora`) VALUES
(1, 'Matutino', '7:00-9:00'),
(3, 'Matutino', '7:00-9:00'),
(4, 'Vespertino', '7:00-9:00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `maestros`
--

CREATE TABLE `maestros` (
  `maestro_id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `apaterno` varchar(70) NOT NULL,
  `amaterno` varchar(70) NOT NULL,
  `email` varchar(120) NOT NULL,
  `carrera` varchar(50) NOT NULL,
  `materia` varchar(500) NOT NULL,
  `grado_estudios` varchar(60) NOT NULL,
  `grupo` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `maestros`
--

INSERT INTO `maestros` (`maestro_id`, `nombre`, `apaterno`, `amaterno`, `email`, `carrera`, `materia`, `grado_estudios`, `grupo`) VALUES
(1, 'Juan', 'Gutierrez', 'Sánchez', 'juan.sánchez9654@maestros.mx', 'Ingeniería en Computación', 'Programación para Internet, Base de Datos', 'Maestría', '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `materias`
--

CREATE TABLE `materias` (
  `materias_id` int(11) NOT NULL,
  `asignatura` varchar(100) NOT NULL,
  `creditos` varchar(15) NOT NULL,
  `semestre` varchar(70) NOT NULL,
  `carrera` varchar(120) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `materias`
--

INSERT INTO `materias` (`materias_id`, `asignatura`, `creditos`, `semestre`, `carrera`) VALUES
(1, 'Programación para Internet', '8', '2024B', 'Ingeniería en Computación'),
(2, 'Base de Datos', '8', '2024B', 'Ingeniería en Computación');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `salones`
--

CREATE TABLE `salones` (
  `salon_id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `edificio` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `salones`
--

INSERT INTO `salones` (`salon_id`, `nombre`, `edificio`) VALUES
(1, 'X10', 'X');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `usuarios_id` int(11) NOT NULL,
  `nombre` varchar(70) NOT NULL,
  `apaterno` varchar(70) NOT NULL,
  `amaterno` varchar(70) NOT NULL,
  `email` varchar(256) NOT NULL,
  `username` varchar(256) NOT NULL,
  `password` varchar(100) NOT NULL,
  `perfil` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`usuarios_id`, `nombre`, `apaterno`, `amaterno`, `email`, `username`, `password`, `perfil`) VALUES
(1, 'Alan', 'Arenas', 'Venegas', '1', 'Developer', 'dev', 'Admin'),
(2, 'Gustavo', 'Arenas', 'Venegas', 'gustavoarenas@gmail.com', 'Gustavo', 'metallica124', 'Rector');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `alumnos`
--
ALTER TABLE `alumnos`
  ADD PRIMARY KEY (`alumnos_id`);

--
-- Indices de la tabla `carreras`
--
ALTER TABLE `carreras`
  ADD PRIMARY KEY (`carrera_id`);

--
-- Indices de la tabla `grupos`
--
ALTER TABLE `grupos`
  ADD PRIMARY KEY (`grupo_id`);

--
-- Indices de la tabla `horarios`
--
ALTER TABLE `horarios`
  ADD PRIMARY KEY (`horario_id`);

--
-- Indices de la tabla `maestros`
--
ALTER TABLE `maestros`
  ADD PRIMARY KEY (`maestro_id`);

--
-- Indices de la tabla `materias`
--
ALTER TABLE `materias`
  ADD PRIMARY KEY (`materias_id`);

--
-- Indices de la tabla `salones`
--
ALTER TABLE `salones`
  ADD PRIMARY KEY (`salon_id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`usuarios_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `alumnos`
--
ALTER TABLE `alumnos`
  MODIFY `alumnos_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `carreras`
--
ALTER TABLE `carreras`
  MODIFY `carrera_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `grupos`
--
ALTER TABLE `grupos`
  MODIFY `grupo_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `horarios`
--
ALTER TABLE `horarios`
  MODIFY `horario_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `maestros`
--
ALTER TABLE `maestros`
  MODIFY `maestro_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `materias`
--
ALTER TABLE `materias`
  MODIFY `materias_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `salones`
--
ALTER TABLE `salones`
  MODIFY `salon_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `usuarios_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
