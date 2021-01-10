-- MySQL dump 10.13  Distrib 5.7.9, for Win64 (x86_64)
--
-- Host: localhost    Database: supermarket
-- ------------------------------------------------------
-- Server version	5.7.10-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('c6b6f577deda');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sms_cats`
--

DROP TABLE IF EXISTS `sms_cats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_cats` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `parent` int(11) DEFAULT NULL,
  `level` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sms_cats`
--

LOCK TABLES `sms_cats` WRITE;
/*!40000 ALTER TABLE `sms_cats` DISABLE KEYS */;
/*!40000 ALTER TABLE `sms_cats` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sms_goods`
--

DROP TABLE IF EXISTS `sms_goods`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_goods` (
  `id` int(11) NOT NULL,
  `intro` varchar(256) DEFAULT NULL,
  `icon` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `sms_goods_ibfk_1` FOREIGN KEY (`id`) REFERENCES `sms_cats` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sms_goods`
--

LOCK TABLES `sms_goods` WRITE;
/*!40000 ALTER TABLE `sms_goods` DISABLE KEYS */;
/*!40000 ALTER TABLE `sms_goods` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sms_orders`
--

DROP TABLE IF EXISTS `sms_orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_orders` (
  `id` bigint(20) NOT NULL,
  `good_id` int(11) NOT NULL,
  `supplier_id` int(11) NOT NULL,
  `price` float NOT NULL,
  `amount` float NOT NULL,
  `datetime` datetime NOT NULL,
  PRIMARY KEY (`id`,`good_id`,`supplier_id`),
  KEY `good_id` (`good_id`),
  KEY `supplier_id` (`supplier_id`),
  CONSTRAINT `sms_orders_ibfk_1` FOREIGN KEY (`good_id`) REFERENCES `sms_goods` (`id`),
  CONSTRAINT `sms_orders_ibfk_2` FOREIGN KEY (`supplier_id`) REFERENCES `sms_suppliers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sms_orders`
--

LOCK TABLES `sms_orders` WRITE;
/*!40000 ALTER TABLE `sms_orders` DISABLE KEYS */;
/*!40000 ALTER TABLE `sms_orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sms_purchase`
--

DROP TABLE IF EXISTS `sms_purchase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_purchase` (
  `good_id` int(11) NOT NULL,
  `supplier_id` int(11) NOT NULL,
  `buildtime` datetime NOT NULL,
  `finishtime` datetime DEFAULT NULL,
  `amount` float NOT NULL,
  `price_in` float NOT NULL,
  `if_finish` tinyint(1) NOT NULL,
  `if_shelf` tinyint(1) NOT NULL,
  PRIMARY KEY (`good_id`,`supplier_id`,`buildtime`),
  KEY `supplier_id` (`supplier_id`),
  CONSTRAINT `sms_purchase_ibfk_1` FOREIGN KEY (`good_id`) REFERENCES `sms_goods` (`id`),
  CONSTRAINT `sms_purchase_ibfk_2` FOREIGN KEY (`supplier_id`) REFERENCES `sms_suppliers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sms_purchase`
--

LOCK TABLES `sms_purchase` WRITE;
/*!40000 ALTER TABLE `sms_purchase` DISABLE KEYS */;
/*!40000 ALTER TABLE `sms_purchase` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sms_roles`
--

DROP TABLE IF EXISTS `sms_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sms_roles`
--

LOCK TABLES `sms_roles` WRITE;
/*!40000 ALTER TABLE `sms_roles` DISABLE KEYS */;
/*!40000 ALTER TABLE `sms_roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sms_sales`
--

DROP TABLE IF EXISTS `sms_sales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_sales` (
  `good_id` int(11) NOT NULL,
  `supplier_id` int(11) NOT NULL,
  `price_out` float NOT NULL,
  `amount` float NOT NULL,
  PRIMARY KEY (`good_id`,`supplier_id`),
  KEY `supplier_id` (`supplier_id`),
  CONSTRAINT `sms_sales_ibfk_1` FOREIGN KEY (`good_id`) REFERENCES `sms_goods` (`id`),
  CONSTRAINT `sms_sales_ibfk_2` FOREIGN KEY (`supplier_id`) REFERENCES `sms_suppliers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sms_sales`
--

LOCK TABLES `sms_sales` WRITE;
/*!40000 ALTER TABLE `sms_sales` DISABLE KEYS */;
/*!40000 ALTER TABLE `sms_sales` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sms_stocks`
--

DROP TABLE IF EXISTS `sms_stocks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_stocks` (
  `good_id` int(11) NOT NULL,
  `supplier_id` int(11) NOT NULL,
  `amount` float NOT NULL,
  PRIMARY KEY (`good_id`,`supplier_id`),
  KEY `supplier_id` (`supplier_id`),
  CONSTRAINT `sms_stocks_ibfk_1` FOREIGN KEY (`good_id`) REFERENCES `sms_goods` (`id`),
  CONSTRAINT `sms_stocks_ibfk_2` FOREIGN KEY (`supplier_id`) REFERENCES `sms_suppliers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sms_stocks`
--

LOCK TABLES `sms_stocks` WRITE;
/*!40000 ALTER TABLE `sms_stocks` DISABLE KEYS */;
/*!40000 ALTER TABLE `sms_stocks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sms_suppliers`
--

DROP TABLE IF EXISTS `sms_suppliers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_suppliers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `mobile` varchar(64) NOT NULL,
  `province` varchar(64) NOT NULL,
  `city` varchar(64) NOT NULL,
  `sign_start` date NOT NULL,
  `sign_end` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sms_suppliers`
--

LOCK TABLES `sms_suppliers` WRITE;
/*!40000 ALTER TABLE `sms_suppliers` DISABLE KEYS */;
/*!40000 ALTER TABLE `sms_suppliers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sms_users`
--

DROP TABLE IF EXISTS `sms_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_users` (
  `id` varchar(64) NOT NULL,
  `password` varchar(64) NOT NULL,
  `name` varchar(64) DEFAULT NULL,
  `gender` varchar(64) DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `mobile` varchar(64) DEFAULT NULL,
  `area` varchar(256) DEFAULT NULL,
  `salary` float DEFAULT NULL,
  `role_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `sms_users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `sms_roles` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sms_users`
--

LOCK TABLES `sms_users` WRITE;
/*!40000 ALTER TABLE `sms_users` DISABLE KEYS */;
/*!40000 ALTER TABLE `sms_users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-01-10 14:20:49
