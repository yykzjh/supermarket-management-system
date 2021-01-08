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
INSERT INTO `alembic_version` VALUES ('65df458fa3f1');
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
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sms_cats`
--

LOCK TABLES `sms_cats` WRITE;
/*!40000 ALTER TABLE `sms_cats` DISABLE KEYS */;
INSERT INTO `sms_cats` VALUES (1,'文具',0,1),(2,'日用品',0,1),(3,'笔',1,2),(4,'本子',1,2),(5,'铅笔',3,3),(6,'毛笔',3,3),(7,'自动铅笔',5,4),(8,'2B铅笔',5,4),(9,'硬毫狼毛笔',6,4),(10,'硬毫鹿毛笔',6,4),(11,'软毫狼毛笔',6,4),(12,'软毫鹿毛笔',6,4),(13,'硬壳本子',4,3),(14,'软壳本子',4,3),(15,'日记本',13,4),(16,'绘画本',13,4),(17,'草稿本',14,4),(18,'作业本',14,4),(19,'洗漱用品',2,2),(20,'清洁用品',2,2),(21,'牙刷',19,3),(22,'毛巾',19,3),(23,'电动牙刷',21,4),(24,'普通牙刷',21,4),(25,'面巾',22,4),(26,'浴巾',22,4),(27,'厨房清洁用品',20,3),(28,'厕所清洁用品',20,3),(29,'清洁剂',27,4),(30,'钢丝球',27,4),(31,'洗碗巾',27,4),(32,'洁厕灵',28,4),(33,'马桶刷',28,4),(34,'皮搋子',28,4),(35,'饮料',0,1),(36,'牛奶',35,2),(37,'纯牛奶',36,3),(44,'蒙牛纯牛奶',37,4);
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
INSERT INTO `sms_goods` VALUES (7,NULL,NULL),(8,NULL,NULL),(9,NULL,NULL),(10,NULL,NULL),(11,NULL,NULL),(12,NULL,NULL),(15,NULL,NULL),(16,NULL,NULL),(17,NULL,NULL),(18,NULL,NULL),(23,NULL,NULL),(24,NULL,NULL),(25,NULL,NULL),(26,NULL,NULL),(29,NULL,NULL),(30,NULL,NULL),(31,NULL,NULL),(32,NULL,NULL),(33,NULL,NULL),(34,NULL,NULL),(44,'蒙牛生产的纯牛奶','2021-01-08/0c51e555e0ed36d0bf32af726bc7d878蒙牛纯牛奶.jpg');
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
INSERT INTO `sms_orders` VALUES (1,7,1,2,2,'2020-11-05 00:00:00'),(1,8,1,1.5,1,'2020-11-05 00:00:00'),(2,7,1,2,3,'2020-11-25 00:00:00'),(3,7,1,2,5,'2020-11-27 00:00:00'),(4,8,1,1.5,10,'2020-12-02 00:00:00');
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
  `amount` float NOT NULL,
  `price_in` float NOT NULL,
  `if_shelf` tinyint(1) NOT NULL,
  `buildtime` datetime NOT NULL,
  `finishtime` datetime DEFAULT NULL,
  `if_finish` tinyint(1) NOT NULL,
  PRIMARY KEY (`good_id`,`supplier_id`),
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
INSERT INTO `sms_purchase` VALUES (7,1,100,1.5,1,'2020-10-02 00:00:00','2020-10-15 00:00:00',1),(8,1,50,1,1,'2020-10-12 00:00:00','2020-11-01 00:00:00',1);
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sms_roles`
--

LOCK TABLES `sms_roles` WRITE;
/*!40000 ALTER TABLE `sms_roles` DISABLE KEYS */;
INSERT INTO `sms_roles` VALUES (2,'admin'),(1,'staff'),(3,'superadmin');
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
  `sign_start` date NOT NULL,
  `sign_end` date NOT NULL,
  `city` varchar(64) NOT NULL,
  `province` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sms_suppliers`
--

LOCK TABLES `sms_suppliers` WRITE;
/*!40000 ALTER TABLE `sms_suppliers` DISABLE KEYS */;
INSERT INTO `sms_suppliers` VALUES (1,'浙江三禾竹木有限公司','12355757562','2014-08-01','2019-08-01','庆元县','浙江省'),(2,'景宁中信实业有限公司','17564546541','2018-12-22','2021-12-22','重庆市','重庆市'),(3,'浙江凤阳山食品有限公司','14546543355','2019-05-22','2022-05-22','龙泉市','浙江省'),(4,'浙江晨光食品食品有限公司','18574566565','2015-12-11','2017-12-11','丽水市','浙江省'),(5,'浙江节节高炭业有限公司','12356565353','2017-01-15','2020-01-15','庆元县','浙江省');
/*!40000 ALTER TABLE `sms_suppliers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sms_users`
--

DROP TABLE IF EXISTS `sms_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_users` (
  `id` varchar(10) NOT NULL,
  `password` varchar(20) NOT NULL,
  `name` varchar(4) DEFAULT NULL,
  `gender` varchar(1) DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `mobile` varchar(11) DEFAULT NULL,
  `area` varchar(128) DEFAULT NULL,
  `salary` int(11) DEFAULT NULL,
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
INSERT INTO `sms_users` VALUES ('2017040391','2017040391','庞志铭','男','1998-12-23','12554456546',NULL,5465,1),('2017040392','2017040392','林鑫','男','1998-12-24','18821664468','5号架',5468,1),('2017040393','2017040393','战伟奇','男','1998-11-11','15346468841','',8483,1),('2017040394','2017040394','钟家辉','男','1998-12-22','18810280617',NULL,8000,3);
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

-- Dump completed on 2021-01-08 16:21:40
