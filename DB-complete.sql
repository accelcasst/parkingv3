
use estacionamiento;

-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 08-12-2023 a las 21:47:57
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `estacionamiento`
--


-- --------------------------------------------------------n n 

--
-- Estructura de tabla para la tabla `carros`
--

CREATE TABLE `carros` (
  `id` int(11) NOT NULL,
  `marca` varchar(45) NOT NULL,
  `modelo` varchar(45) NOT NULL,
  `year` varchar(45) NOT NULL,
  `color` varchar(45) NOT NULL,
  `entrada` varchar(20) NOT NULL,
  `salida` datetime NOT NULL,
  `foto` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `carros`
--

INSERT INTO `carros` (`id`, `marca`, `modelo`, `year`, `color`, `entrada`, `salida`, `foto`) VALUES
(1, 'Nissan', 'Tsuru', '2010', 'Verde', '0000-00-00 ', '0000-00-00 00:00:00', '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cars`
--

CREATE TABLE `cars` (
  `id` int(11) NOT NULL,
  `Placa` varchar(20) NOT NULL,
  `entry_time` datetime DEFAULT NULL,
  `exit_time` datetime DEFAULT NULL,
  `id_sucursal` int(11) NOT NULL,
  `estado` varchar(15) NOT NULL,
  `qr_image_path` text NOT NULL,
  `total` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `cars`
--

INSERT INTO `cars` (`id`, `Placa`, `entry_time`, `exit_time`, `id_sucursal`, `estado`, `qr_image_path`, `total`) VALUES
(39, 'BRPS', '2023-11-25 18:26:00', '2023-11-25 21:26:00', 1, 'Pagado', 'D:\\proyecto-nuevo\\qrcodes\\qr_39.png', 40),
(44, 'PLACA123', '2023-11-26 20:20:00', '2023-11-26 22:24:00', 1, 'Pagado', 'D:\\proyecto-nuevo\\qrcodes\\qr_44.png', 20),
(45, 'UBGFD', '2023-12-03 15:25:00', '2023-12-03 20:26:00', 1, 'Pagado', 'D:\\proyecto-nuevo\\qrcodes\\qr_45.png', 100),
(46, 'ZXCVB', '2023-12-03 15:33:00', '2023-12-04 19:55:00', 1, 'Pagado', 'D:\\proyecto-nuevo\\qrcodes\\qr_46.png', 580),
(51, '1234567', '2023-12-03 16:26:00', '2023-12-03 21:35:00', 1, 'Pagado', 'D:\\proyecto-nuevo\\qrcodes\\qr_51.png', 100),
(56, '99999999', '2023-12-03 19:31:00', NULL, 1, 'no pagado', 'D:\\proyecto-nuevo\\qrcodes\\qr_56.png', 0),
(57, 'PLACA66666', '2023-12-03 20:26:00', '2023-12-03 23:39:00', 1, 'Pagado', 'D:\\proyecto-nuevo\\qrcodes\\qr_57.png', 40),
(58, 'PLACAOaxtepec', '2023-12-03 21:04:00', '2023-12-03 23:05:00', 11, 'Pagado', 'D:\\proyecto-nuevo\\qrcodes\\qr_58.png', 20),
(59, 'oaxtepec', '2023-12-04 21:06:00', '2023-12-04 21:19:00', 11, 'Pagado', 'D:\\proyecto-nuevo\\qrcodes\\qr_59.png', 0),
(60, 'placa3456', '2023-12-04 12:00:00', NULL, 11, 'no pagado', 'D:\\proyecto-nuevo\\qrcodes\\qr_60.png', 0),
(61, 'Teques', '2023-12-03 21:16:00', '2023-12-03 00:16:00', 13, 'Pagado', 'D:\\proyecto-nuevo\\qrcodes\\qr_61.png', 0),
(62, 'BBBBB', '2023-12-08 14:01:00', NULL, 1, 'no pagado', 'D:\\proyecto-nuevo\\qrcodes\\qr_62.png', 0),
(63, 'prueba342', '2023-12-08 14:31:00', NULL, 1, 'no pagado', 'D:\\proyecto-nuevo\\qrcodes\\qr_63.png', 0),
(64, 'RRRRRprueba', '2023-12-08 18:33:00', NULL, 1, 'no pagado', 'D:\\proyecto-nuevo\\qrcodes\\qr_64.png', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estacionamiento`
--

CREATE TABLE `estacionamiento` (
  `id` int(11) NOT NULL,
  `placa` varchar(200) NOT NULL,
  `color` varchar(200) NOT NULL,
  `marca` varchar(200) NOT NULL,
  `Entrada` datetime NOT NULL,
  `Salida` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `estacionamiento`
--

INSERT INTO `estacionamiento` (`id`, `placa`, `color`, `marca`, `Entrada`, `Salida`) VALUES
(1, 'AAAAA', 'VERDE', 'FORD', '2023-11-11 13:49:25', '2023-11-11 15:49:25');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pension`
--

CREATE TABLE `pension` (
  `id` int(11) NOT NULL,
  `placa` varchar(100) NOT NULL,
  `fecha_entrada` datetime NOT NULL,
  `fecha_salida` datetime NOT NULL,
  `id_sucursal` int(100) NOT NULL,
  `qr_image_path` varchar(250) NOT NULL,
  `total` float NOT NULL,
  `estado` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pension`
--

INSERT INTO `pension` (`id`, `placa`, `fecha_entrada`, `fecha_salida`, `id_sucursal`, `qr_image_path`, `total`, `estado`) VALUES
(1, 'UJHBGFD', '2023-11-26 09:25:32', '2024-04-30 18:24:00', 0, '', 29108.3, ''),
(10, 'GGGG', '2023-11-26 20:25:00', '2024-02-29 18:11:00', 0, 'D:\\proyecto-nuevo\\qrcodes\\qr_10.png', 4000, ''),
(12, 'OOOOOOOOO', '2023-12-03 18:50:00', '2024-03-26 20:41:00', 0, 'D:\\proyecto-nuevo\\qrcodes\\qr_12.png', 20000, ''),
(13, 'IIIIIIIIIII', '2023-12-03 20:41:00', '2024-02-03 20:48:00', 0, 'D:\\proyecto-nuevo\\qrcodes\\qr_13.png', 8000, ''),
(15, 'CarroNuevo', '2023-12-03 20:49:00', '2024-02-03 20:59:00', 0, 'D:\\proyecto-nuevo\\qrcodes\\qr_15.png', 8000, ''),
(16, 'Carronuevo2', '2023-12-03 21:02:00', '2024-02-03 21:03:00', 0, 'D:\\proyecto-nuevo\\qrcodes\\qr_16.png', 8000, '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

CREATE TABLE `roles` (
  `id_rol` int(11) NOT NULL,
  `descripcion` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `roles`
--

INSERT INTO `roles` (`id_rol`, `descripcion`) VALUES
(1, 'admin'),
(2, 'usuario'),
(3, 'Super admin');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sucursal`
--

CREATE TABLE `sucursal` (
  `id_sucursal` int(11) NOT NULL,
  `descripcion` varchar(100) NOT NULL,
  `codigop` varchar(6) NOT NULL,
  `telefono` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `sucursal`
--

INSERT INTO `sucursal` (`id_sucursal`, `descripcion`, `codigop`, `telefono`) VALUES
(1, 'Temixco', '62763', '777-123-4856'),
(2, 'Emiliano zapata', '99999', '777-123-4856'),
(3, 'Cuernavaca', '33333', '777-123-4856'),
(10, 'xochitepec', '62763', '777-796-4871'),
(11, 'Oaxtepec', '96548', '777-888-9999'),
(13, 'Teques', '55555', '999-632-8965');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `id_rol` int(11) NOT NULL,
  `id_sucursal` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `username`, `correo`, `password`, `id_rol`, `id_sucursal`) VALUES
(2, 'Alejandra', 'ale@gmail.com', '123', 1, 1),
(6, 'aldahir', 'alda@gmail.com', '123', 3, 1),
(25, 'administrador', 'admin@gmail.com', '123', 1, 11),
(26, 'usuariox', 'usuario@gmail.com', '123', 2, 11),
(27, 'Hector', 'hec@gmail.com', '123', 2, 11),
(28, 'Gael', 'gael@gmail.com', '123', 1, 13),
(29, 'Lulu', 'lulu@gmail.com', '123', 2, 13);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `carros`
--
ALTER TABLE `carros`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `cars`
--
ALTER TABLE `cars`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `estacionamiento`
--
ALTER TABLE `estacionamiento`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `pension`
--
ALTER TABLE `pension`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id_rol`);

--
-- Indices de la tabla `sucursal`
--
ALTER TABLE `sucursal`
  ADD PRIMARY KEY (`id_sucursal`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_rol` (`id_rol`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `carros`
--
ALTER TABLE `carros`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `cars`
--
ALTER TABLE `cars`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=65;

--
-- AUTO_INCREMENT de la tabla `estacionamiento`
--
ALTER TABLE `estacionamiento`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `pension`
--
ALTER TABLE `pension`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `id_rol` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `sucursal`
--
ALTER TABLE `sucursal`
  MODIFY `id_sucursal` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
