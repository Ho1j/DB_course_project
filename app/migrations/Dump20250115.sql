CREATE DATABASE  IF NOT EXISTS `airline_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `airline_db`;
-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: airline_db
-- ------------------------------------------------------
-- Server version	8.0.39

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `airports`
--

DROP TABLE IF EXISTS `airports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `airports` (
  `airport_id` int NOT NULL AUTO_INCREMENT,
  `airport_code` varchar(10) DEFAULT NULL,
  `airport_name` varchar(100) NOT NULL,
  `city` varchar(50) NOT NULL,
  `country` varchar(50) NOT NULL,
  PRIMARY KEY (`airport_id`),
  UNIQUE KEY `airport_code` (`airport_code`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `airports`
--

LOCK TABLES `airports` WRITE;
/*!40000 ALTER TABLE `airports` DISABLE KEYS */;
INSERT INTO `airports` VALUES (1,'JFK','John F. Kennedy International Airport','New York','USA'),(2,'SVO','Sheremetyevo International Airport','Moscow','Russia'),(3,'LHR','London Heathrow Airport','London','UK'),(12,'IST','Istanbul Airport','Istanbul','Turkey'),(13,'DME','Domodedovo International Airport','Moscow','Russia'),(14,'LED','Pulkovo Airport','Saint Petersburg','Russia'),(15,'KZN','Kazan International Airport','Kazan','Russia');
/*!40000 ALTER TABLE `airports` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `canceled_tickets`
--

DROP TABLE IF EXISTS `canceled_tickets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `canceled_tickets` (
  `ticket_id` int NOT NULL,
  `order_id` int NOT NULL,
  `schedule_id` int NOT NULL,
  `passport` varchar(50) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `birth_date` date NOT NULL,
  `seat_number` varchar(10) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `status` varchar(20) NOT NULL DEFAULT 'canceled',
  PRIMARY KEY (`ticket_id`),
  KEY `fk_canceled_order` (`order_id`),
  KEY `fk_canceled_schedule` (`schedule_id`),
  CONSTRAINT `fk_canceled_order` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_canceled_schedule` FOREIGN KEY (`schedule_id`) REFERENCES `schedules` (`schedule_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `canceled_tickets`
--

LOCK TABLES `canceled_tickets` WRITE;
/*!40000 ALTER TABLE `canceled_tickets` DISABLE KEYS */;
INSERT INTO `canceled_tickets` VALUES (14,47,1,'000000000','Bob','Marley','1945-02-06','4A',300.00,'canceled'),(17,64,1,'555555556','M','S','2003-12-25','1A',300.00,'canceled'),(20,71,1,'111111111','N','S','2003-12-25','10A',300.00,'canceled'),(21,72,1,'333333333','m','s','2003-12-25','10A',300.00,'canceled'),(22,73,1,'222222221','M','s','2003-12-25','1A',300.00,'canceled'),(23,74,1,'888888888','s','s','2025-01-14','10A',300.00,'canceled');
/*!40000 ALTER TABLE `canceled_tickets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cashiers`
--

DROP TABLE IF EXISTS `cashiers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cashiers` (
  `cashier_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `passport_data` varchar(50) NOT NULL,
  `hire_date` date NOT NULL,
  `termination_date` date DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`cashier_id`),
  UNIQUE KEY `passport_data` (`passport_data`),
  KEY `fk_cashiers_user_id` (`user_id`),
  CONSTRAINT `fk_cashiers_user_id` FOREIGN KEY (`user_id`) REFERENCES `internal_users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cashiers`
--

LOCK TABLES `cashiers` WRITE;
/*!40000 ALTER TABLE `cashiers` DISABLE KEYS */;
INSERT INTO `cashiers` VALUES (1,'Michael','Jones','627176510','2025-01-01',NULL,2),(3,'John','Doe','123242424','2024-12-01','2025-01-14',4);
/*!40000 ALTER TABLE `cashiers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cashiers_sales_report`
--

DROP TABLE IF EXISTS `cashiers_sales_report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cashiers_sales_report` (
  `report_id` int NOT NULL AUTO_INCREMENT,
  `cashier_id` int NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `total_sales` decimal(10,2) DEFAULT NULL,
  `total_tickets` int NOT NULL,
  `period` date NOT NULL,
  PRIMARY KEY (`report_id`),
  UNIQUE KEY `unique_cashier_period` (`cashier_id`,`period`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cashiers_sales_report`
--

LOCK TABLES `cashiers_sales_report` WRITE;
/*!40000 ALTER TABLE `cashiers_sales_report` DISABLE KEYS */;
INSERT INTO `cashiers_sales_report` VALUES (1,1,'Michael','Jones',300.00,1,'2025-01-01'),(2,1,'Michael','Jones',300.00,1,'2024-12-01');
/*!40000 ALTER TABLE `cashiers_sales_report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `destinations_report`
--

DROP TABLE IF EXISTS `destinations_report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `destinations_report` (
  `report_id` int NOT NULL AUTO_INCREMENT,
  `country` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `total_flights` int NOT NULL,
  `period` date NOT NULL,
  PRIMARY KEY (`report_id`),
  UNIQUE KEY `unique_period_country` (`country`,`period`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `destinations_report`
--

LOCK TABLES `destinations_report` WRITE;
/*!40000 ALTER TABLE `destinations_report` DISABLE KEYS */;
INSERT INTO `destinations_report` VALUES (1,'USA',3,'2025-02-01'),(2,'UK',2,'2025-02-01');
/*!40000 ALTER TABLE `destinations_report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `external_users`
--

DROP TABLE IF EXISTS `external_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `external_users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `login` varchar(30) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `user_group` varchar(10) NOT NULL DEFAULT 'user',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `login` (`login`),
  UNIQUE KEY `email` (`email`),
  CONSTRAINT `external_users_chk_1` CHECK ((`user_group` = _utf8mb4'user'))
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `external_users`
--

LOCK TABLES `external_users` WRITE;
/*!40000 ALTER TABLE `external_users` DISABLE KEYS */;
INSERT INTO `external_users` VALUES (1,'test@mail.com','scrypt:32768:8:1$7y7XTN6bkILw4uRi$0b7f7a8dd5ddeb0e24915b412d76097f39748f82d6638b91c887f7ba4765bffce0ffde42f5eef526571e12b187c9d29050b64f0699831a7b8fdbb0348f724584','test@mail.com','user'),(2,'test2','scrypt:32768:8:1$Ufh2khDz3deGXQKM$e2935e6580796a4031c2ad1bc21280b4ac4e69b8a7d4d6f51a1437cb13c913ed8bc860ba9416a02c2e50b8fcdc3bdadbb81290474edb8e85f79338bedc4f4a3b','test2@mail.com','user'),(3,'test3','scrypt:32768:8:1$mTfdrLDg8wC8bBjF$092cd1c4fa36130fe3c40d2c8998470c1230ec516387891137fef2bdc807d033150262b525e34c5e3da4b9013d386ce49680c9282373c3363a72142bd74e7f14','test3@mail.com','user');
/*!40000 ALTER TABLE `external_users` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `orders_email_update` AFTER UPDATE ON `external_users` FOR EACH ROW BEGIN
    IF NEW.email <> OLD.email THEN
        UPDATE `orders`
        SET `email` = NEW.email
        WHERE `email` = OLD.email;
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `flights`
--

DROP TABLE IF EXISTS `flights`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flights` (
  `flight_id` int NOT NULL AUTO_INCREMENT,
  `flight_number` varchar(10) NOT NULL,
  `departure_airport_id` int NOT NULL,
  `arrival_airport_id` int NOT NULL,
  `departure_time` time NOT NULL,
  `arrival_time` time NOT NULL,
  `days` set('Mon','Tue','Wed','Thu','Fri','Sat','Sun') NOT NULL,
  `ticket_price` decimal(10,2) NOT NULL,
  `total_tickets` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`flight_id`),
  UNIQUE KEY `flight_number` (`flight_number`),
  KEY `departure_airport_id` (`departure_airport_id`),
  KEY `arrival_airport_id` (`arrival_airport_id`),
  CONSTRAINT `flights_ibfk_1` FOREIGN KEY (`departure_airport_id`) REFERENCES `airports` (`airport_id`),
  CONSTRAINT `flights_ibfk_2` FOREIGN KEY (`arrival_airport_id`) REFERENCES `airports` (`airport_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flights`
--

LOCK TABLES `flights` WRITE;
/*!40000 ALTER TABLE `flights` DISABLE KEYS */;
INSERT INTO `flights` VALUES (1,'SU1000',2,1,'10:00:00','14:00:00','Mon,Wed,Fri',300.00,0),(2,'SU2000',2,3,'12:00:00','14:30:00','Tue,Thu,Sat',150.00,0),(3,'BA3000',3,1,'15:00:00','19:00:00','Mon',200.00,0);
/*!40000 ALTER TABLE `flights` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flights_revenue_report`
--

DROP TABLE IF EXISTS `flights_revenue_report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flights_revenue_report` (
  `id` int NOT NULL AUTO_INCREMENT,
  `flight_number` varchar(10) NOT NULL,
  `total_revenue` decimal(10,2) NOT NULL,
  `total_tickets` int NOT NULL,
  `period` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flights_revenue_report`
--

LOCK TABLES `flights_revenue_report` WRITE;
/*!40000 ALTER TABLE `flights_revenue_report` DISABLE KEYS */;
INSERT INTO `flights_revenue_report` VALUES (1,'SU1000',300.00,1,'2025-02-01');
/*!40000 ALTER TABLE `flights_revenue_report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `internal_users`
--

DROP TABLE IF EXISTS `internal_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `internal_users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `login` varchar(30) NOT NULL,
  `password` varchar(255) NOT NULL,
  `user_group` enum('cashier','manager') DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `login` (`login`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `internal_users`
--

LOCK TABLES `internal_users` WRITE;
/*!40000 ALTER TABLE `internal_users` DISABLE KEYS */;
INSERT INTO `internal_users` VALUES (2,'cashier1','cashier1','cashier'),(3,'manager1','manager1','manager'),(4,'cashier2','cashier2','cashier');
/*!40000 ALTER TABLE `internal_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) DEFAULT NULL,
  `booking_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `cashier_id` int DEFAULT NULL,
  `last_updated` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_orders_cashier_id` (`cashier_id`),
  CONSTRAINT `fk_orders_cashier_id` FOREIGN KEY (`cashier_id`) REFERENCES `cashiers` (`cashier_id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=77 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (47,'test3@mail.com','2024-12-13 00:46:38',1,'2025-01-14 18:04:17'),(64,'test3@mail.com','2025-01-13 19:17:13',1,'2025-01-13 19:17:13'),(71,'test3@mail.com','2025-01-14 00:29:04',1,'2025-01-14 00:29:04'),(72,'test3@mail.com','2025-01-14 01:23:35',1,'2025-01-14 01:23:35'),(73,'test3@mail.com','2025-01-14 01:33:00',1,'2025-01-14 01:33:00'),(74,'test3@mail.com','2025-01-14 03:05:11',1,'2025-01-14 03:05:11');
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `schedules`
--

DROP TABLE IF EXISTS `schedules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `schedules` (
  `schedule_id` int NOT NULL AUTO_INCREMENT,
  `flight_id` int NOT NULL,
  `schedule_date` date NOT NULL,
  `available_tickets` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`schedule_id`),
  KEY `flight_id` (`flight_id`),
  CONSTRAINT `schedules_ibfk_1` FOREIGN KEY (`flight_id`) REFERENCES `flights` (`flight_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schedules`
--

LOCK TABLES `schedules` WRITE;
/*!40000 ALTER TABLE `schedules` DISABLE KEYS */;
INSERT INTO `schedules` VALUES (1,1,'2025-02-03',198),(3,1,'2025-02-07',0),(4,2,'2025-02-04',0),(5,2,'2025-02-06',0),(6,3,'2025-02-03',0);
/*!40000 ALTER TABLE `schedules` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `set_available_tickets` BEFORE INSERT ON `schedules` FOR EACH ROW BEGIN
  DECLARE totalTickets INT;

  -- Получаем общее количество билетов для рейса
  SELECT `total_tickets` INTO totalTickets
  FROM `flights`
  WHERE `flight_id` = NEW.`flight_id`;

  -- Устанавливаем значение available_tickets
  SET NEW.`available_tickets` = totalTickets;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `tickets`
--

DROP TABLE IF EXISTS `tickets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tickets` (
  `ticket_id` int NOT NULL AUTO_INCREMENT,
  `order_id` int NOT NULL,
  `schedule_id` int NOT NULL,
  `passport` varchar(50) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `birth_date` date NOT NULL,
  `seat_number` varchar(10) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `status` enum('confirmed') NOT NULL DEFAULT 'confirmed',
  PRIMARY KEY (`ticket_id`),
  UNIQUE KEY `unique_schedule_passport` (`passport`,`schedule_id`),
  UNIQUE KEY `unique_schedule_seat` (`schedule_id`,`seat_number`),
  KEY `tickets_ibfk_2` (`order_id`),
  CONSTRAINT `tickets_ibfk_1` FOREIGN KEY (`schedule_id`) REFERENCES `schedules` (`schedule_id`) ON DELETE CASCADE,
  CONSTRAINT `tickets_ibfk_2` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tickets`
--

LOCK TABLES `tickets` WRITE;
/*!40000 ALTER TABLE `tickets` DISABLE KEYS */;
INSERT INTO `tickets` VALUES (25,47,1,'222222221','denic','chveleu','2000-12-01','',300.00,'confirmed');
/*!40000 ALTER TABLE `tickets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'airline_db'
--

--
-- Dumping routines for database 'airline_db'
--
/*!50003 DROP PROCEDURE IF EXISTS `CreateCashiersSalesReport` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `CreateCashiersSalesReport`(
    IN sales_month DATE -- Format: 'YYYY-MM-01'
)
BEGIN
    -- Check if records for the specified month already exist
    IF EXISTS (
        SELECT 1
        FROM cashiers_sales_report
        WHERE period = DATE_FORMAT(sales_month, '%Y-%m-01')
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Data for the specified month already exists in the table cashier_sales_report';
    ELSE
        -- Insert data into the cashier_sales_report table
        INSERT INTO cashiers_sales_report (cashier_id, first_name, last_name, total_sales, total_tickets, period)
        SELECT 
            c.cashier_id, 
            c.first_name,
            c.last_name,
            SUM(t.price) AS total_sales,
            COUNT(t.ticket_id) AS total_tickets,
            DATE_FORMAT(sales_month, '%Y-%m-01') AS period
        FROM tickets t
        JOIN orders o ON o.id = t.order_id
        JOIN cashiers c ON c.cashier_id = o.cashier_id
        WHERE DATE_FORMAT(o.booking_date, '%Y-%m') = DATE_FORMAT(sales_month, '%Y-%m')
        GROUP BY c.cashier_id, c.first_name, c.last_name
        ORDER BY total_sales DESC;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `CreateDestinationsReport` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `CreateDestinationsReport`(
    IN sales_month DATE -- Format: 'YYYY-MM-01'
)
BEGIN
    -- Check if records for the specified month already exist
    IF EXISTS (
        SELECT 1
        FROM destinations_report
        WHERE period = DATE_FORMAT(sales_month, '%Y-%m-01')
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Data for the specified month already exists in the table destination_sales_report';
    ELSE
        -- Insert data into the destination_sales_report table
        INSERT INTO destinations_report (country, total_flights, period)
        SELECT 
            a.country, 
            COUNT(s.schedule_id) AS total_flights,
            DATE_FORMAT(sales_month, '%Y-%m-01') AS period
        FROM schedules s
        JOIN flights f ON f.flight_id = s.flight_id
        JOIN airports a ON a.airport_id = f.arrival_airport_id
        WHERE DATE_FORMAT(s.schedule_date, '%Y-%m') = DATE_FORMAT(sales_month, '%Y-%m')
        GROUP BY a.country
        ORDER BY total_flights DESC;
    END IF;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `CreateFlightsRevenueReport` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `CreateFlightsRevenueReport`(
    IN revenue_month DATE -- Формат: 'YYYY-MM-01'
)
BEGIN
    -- Проверяем, существуют ли записи за указанный месяц
    IF EXISTS (
        SELECT 1
        FROM flights_revenue_report
        WHERE period = DATE_FORMAT(revenue_month, '%Y-%m-01')
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Данные за указанный месяц уже существуют в таблице flights_revenue_report';
    ELSE
        -- Вставляем данные в таблицу flights_revenue_report
        INSERT INTO flights_revenue_report (flight_number, total_revenue, total_tickets, period)
        SELECT 
            f.flight_number, 
            SUM(t.price) AS total_revenue,
            COUNT(t.ticket_id) AS total_tickets,
            DATE_FORMAT(revenue_month, '%Y-%m-01') AS period
        FROM tickets t
        JOIN schedules s ON s.schedule_id = t.schedule_id
        JOIN flights f ON f.flight_id = s.flight_id
        WHERE DATE_FORMAT(s.schedule_date, '%Y-%m') = DATE_FORMAT(revenue_month, '%Y-%m')
        GROUP BY f.flight_number
        ORDER BY total_revenue DESC;
    END IF;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-15 11:32:45
