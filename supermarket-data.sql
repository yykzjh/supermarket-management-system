/*
 Navicat Premium Data Transfer

 Source Server         : mysql
 Source Server Type    : MySQL
 Source Server Version : 80018
 Source Host           : localhost:3306
 Source Schema         : supermarket

 Target Server Type    : MySQL
 Target Server Version : 80018
 File Encoding         : 65001

 Date: 11/01/2021 19:01:16
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for alembic_version
-- ----------------------------
DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- ----------------------------
-- Records of alembic_version
-- ----------------------------
BEGIN;
INSERT INTO `alembic_version` VALUES ('c6b6f577deda');
COMMIT;

-- ----------------------------
-- Table structure for sms_cats
-- ----------------------------
DROP TABLE IF EXISTS `sms_cats`;
CREATE TABLE `sms_cats` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `parent` int(11) DEFAULT NULL,
  `level` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=82 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- ----------------------------
-- Records of sms_cats
-- ----------------------------
BEGIN;
INSERT INTO `sms_cats` VALUES (1, '食品', 0, 1);
INSERT INTO `sms_cats` VALUES (2, '文具', 0, 1);
INSERT INTO `sms_cats` VALUES (3, '电器', 0, 1);
INSERT INTO `sms_cats` VALUES (5, '清洁用品', 0, 1);
INSERT INTO `sms_cats` VALUES (6, '果蔬生鲜', 1, 2);
INSERT INTO `sms_cats` VALUES (7, '零食', 1, 2);
INSERT INTO `sms_cats` VALUES (8, '饮品', 1, 2);
INSERT INTO `sms_cats` VALUES (9, '方便速食', 1, 2);
INSERT INTO `sms_cats` VALUES (10, '厨房调味品', 1, 2);
INSERT INTO `sms_cats` VALUES (11, '水果', 6, 3);
INSERT INTO `sms_cats` VALUES (12, '蔬菜', 6, 3);
INSERT INTO `sms_cats` VALUES (13, '生鲜', 6, 3);
INSERT INTO `sms_cats` VALUES (14, '苹果', 11, 4);
INSERT INTO `sms_cats` VALUES (15, '橙子', 11, 4);
INSERT INTO `sms_cats` VALUES (16, '榴莲', 11, 4);
INSERT INTO `sms_cats` VALUES (17, '香蕉', 11, 4);
INSERT INTO `sms_cats` VALUES (18, '白菜', 12, 4);
INSERT INTO `sms_cats` VALUES (19, '土豆', 12, 4);
INSERT INTO `sms_cats` VALUES (20, '带鱼', 13, 4);
INSERT INTO `sms_cats` VALUES (21, '虾', 13, 4);
INSERT INTO `sms_cats` VALUES (22, '猪肉', 13, 4);
INSERT INTO `sms_cats` VALUES (23, '羊肉', 13, 4);
INSERT INTO `sms_cats` VALUES (24, '饼干', 7, 3);
INSERT INTO `sms_cats` VALUES (26, '巧克力', 7, 3);
INSERT INTO `sms_cats` VALUES (27, '辣条', 7, 3);
INSERT INTO `sms_cats` VALUES (28, '薯片', 7, 3);
INSERT INTO `sms_cats` VALUES (29, '旺旺仙贝', 24, 4);
INSERT INTO `sms_cats` VALUES (30, '卫龙辣棒', 27, 4);
INSERT INTO `sms_cats` VALUES (31, '茶', 8, 3);
INSERT INTO `sms_cats` VALUES (32, '牛奶', 8, 3);
INSERT INTO `sms_cats` VALUES (33, '饮料', 8, 3);
INSERT INTO `sms_cats` VALUES (34, '茉莉花茶', 31, 4);
INSERT INTO `sms_cats` VALUES (35, '绿茶', 31, 4);
INSERT INTO `sms_cats` VALUES (37, '蒙牛纯牛奶', 32, 4);
INSERT INTO `sms_cats` VALUES (38, '纯甄酸牛奶', 32, 4);
INSERT INTO `sms_cats` VALUES (39, '伊利红枣酸奶', 32, 4);
INSERT INTO `sms_cats` VALUES (40, '百事可乐', 33, 4);
INSERT INTO `sms_cats` VALUES (41, '统一冰红茶', 33, 4);
INSERT INTO `sms_cats` VALUES (43, '火腿肠', 9, 3);
INSERT INTO `sms_cats` VALUES (45, '盐', 10, 3);
INSERT INTO `sms_cats` VALUES (46, '醋', 10, 3);
INSERT INTO `sms_cats` VALUES (47, '本子', 2, 2);
INSERT INTO `sms_cats` VALUES (48, '笔', 2, 2);
INSERT INTO `sms_cats` VALUES (49, '学习机', 2, 2);
INSERT INTO `sms_cats` VALUES (50, '软抄本', 47, 3);
INSERT INTO `sms_cats` VALUES (51, '硬皮本', 47, 3);
INSERT INTO `sms_cats` VALUES (52, '作文本', 50, 4);
INSERT INTO `sms_cats` VALUES (53, '手账本', 51, 4);
INSERT INTO `sms_cats` VALUES (54, '铅笔', 48, 3);
INSERT INTO `sms_cats` VALUES (55, '钢笔', 48, 3);
INSERT INTO `sms_cats` VALUES (56, '中性笔', 48, 3);
INSERT INTO `sms_cats` VALUES (58, '英雄钢笔', 55, 4);
INSERT INTO `sms_cats` VALUES (59, '晨光', 56, 4);
INSERT INTO `sms_cats` VALUES (60, '步步高', 49, 3);
INSERT INTO `sms_cats` VALUES (61, '小天才', 49, 3);
INSERT INTO `sms_cats` VALUES (62, '平板学习机', 59, 4);
INSERT INTO `sms_cats` VALUES (63, '厨房电器', 3, 2);
INSERT INTO `sms_cats` VALUES (64, '榨汁机', 63, 3);
INSERT INTO `sms_cats` VALUES (65, '豆浆机', 63, 3);
INSERT INTO `sms_cats` VALUES (66, '九阳豆浆机', 65, 4);
INSERT INTO `sms_cats` VALUES (67, '厨房清洁', 5, 2);
INSERT INTO `sms_cats` VALUES (68, '浴室清洁', 5, 2);
INSERT INTO `sms_cats` VALUES (70, '洗涤灵', 67, 3);
INSERT INTO `sms_cats` VALUES (71, '立白', 70, 4);
INSERT INTO `sms_cats` VALUES (72, '蓝猫', 70, 4);
INSERT INTO `sms_cats` VALUES (73, '洁厕灵', 68, 3);
INSERT INTO `sms_cats` VALUES (74, '威猛先生', 73, 4);
INSERT INTO `sms_cats` VALUES (75, '乐事薯片', 28, 4);
INSERT INTO `sms_cats` VALUES (77, '大鸭梨', 11, 4);
INSERT INTO `sms_cats` VALUES (80, 'shng', 54, 4);
COMMIT;

-- ----------------------------
-- Table structure for sms_goods
-- ----------------------------
DROP TABLE IF EXISTS `sms_goods`;
CREATE TABLE `sms_goods` (
  `id` int(11) NOT NULL,
  `intro` varchar(256) DEFAULT NULL,
  `icon` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `sms_goods_ibfk_1` FOREIGN KEY (`id`) REFERENCES `sms_cats` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- ----------------------------
-- Records of sms_goods
-- ----------------------------
BEGIN;
INSERT INTO `sms_goods` VALUES (14, NULL, NULL);
INSERT INTO `sms_goods` VALUES (15, NULL, NULL);
INSERT INTO `sms_goods` VALUES (16, NULL, NULL);
INSERT INTO `sms_goods` VALUES (17, NULL, NULL);
INSERT INTO `sms_goods` VALUES (18, NULL, NULL);
INSERT INTO `sms_goods` VALUES (19, NULL, NULL);
INSERT INTO `sms_goods` VALUES (20, NULL, NULL);
INSERT INTO `sms_goods` VALUES (21, NULL, NULL);
INSERT INTO `sms_goods` VALUES (22, NULL, NULL);
INSERT INTO `sms_goods` VALUES (23, NULL, NULL);
INSERT INTO `sms_goods` VALUES (29, NULL, NULL);
INSERT INTO `sms_goods` VALUES (30, NULL, NULL);
INSERT INTO `sms_goods` VALUES (34, NULL, NULL);
INSERT INTO `sms_goods` VALUES (35, NULL, NULL);
INSERT INTO `sms_goods` VALUES (37, NULL, NULL);
INSERT INTO `sms_goods` VALUES (38, NULL, NULL);
INSERT INTO `sms_goods` VALUES (39, NULL, NULL);
INSERT INTO `sms_goods` VALUES (40, NULL, NULL);
INSERT INTO `sms_goods` VALUES (41, NULL, NULL);
INSERT INTO `sms_goods` VALUES (52, NULL, NULL);
INSERT INTO `sms_goods` VALUES (53, NULL, NULL);
INSERT INTO `sms_goods` VALUES (58, NULL, NULL);
INSERT INTO `sms_goods` VALUES (59, NULL, NULL);
INSERT INTO `sms_goods` VALUES (62, NULL, NULL);
INSERT INTO `sms_goods` VALUES (66, NULL, NULL);
INSERT INTO `sms_goods` VALUES (71, NULL, NULL);
INSERT INTO `sms_goods` VALUES (72, NULL, NULL);
INSERT INTO `sms_goods` VALUES (74, NULL, NULL);
INSERT INTO `sms_goods` VALUES (75, '<p>乐事薯片比其他薯片好吃，很薄很脆</p>', '2021-01-10/13e9ecb5b53935bda9ec088415fd74b8chips.jpeg');
INSERT INTO `sms_goods` VALUES (77, 'yummy，真的好吃，美味又营养，全家人都爱吃，哈哈哈哈', '2021-01-11/97d23c5495e73f6c81d241f7be966b55lili.jpeg');
INSERT INTO `sms_goods` VALUES (80, '<p>yunny</p>', '2021-01-11/13e9ecb5b53935bda9ec088415fd74b8chips.jpeg');
COMMIT;

-- ----------------------------
-- Table structure for sms_orders
-- ----------------------------
DROP TABLE IF EXISTS `sms_orders`;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- ----------------------------
-- Records of sms_orders
-- ----------------------------
BEGIN;
INSERT INTO `sms_orders` VALUES (1, 14, 34, 4.5, 2, '2020-10-11 00:01:57');
INSERT INTO `sms_orders` VALUES (1, 15, 34, 3, 1, '2020-10-11 00:01:57');
INSERT INTO `sms_orders` VALUES (1, 16, 38, 5.2, 3, '2020-10-11 00:01:57');
INSERT INTO `sms_orders` VALUES (2, 22, 38, 3.2, 1, '2020-08-11 00:06:43');
INSERT INTO `sms_orders` VALUES (2, 23, 33, 2.8, 2, '2020-08-11 00:06:43');
INSERT INTO `sms_orders` VALUES (2, 30, 35, 7, 10, '2020-08-11 00:06:43');
INSERT INTO `sms_orders` VALUES (2, 35, 32, 12, 5, '2020-08-11 00:06:43');
INSERT INTO `sms_orders` VALUES (3, 40, 35, 6, 4, '2020-05-11 00:37:56');
INSERT INTO `sms_orders` VALUES (4, 17, 38, 3.8, 7, '2020-01-15 00:03:48');
INSERT INTO `sms_orders` VALUES (4, 52, 36, 8, 9, '2020-04-11 00:39:19');
INSERT INTO `sms_orders` VALUES (5, 18, 34, 4.5, 9, '2020-07-08 00:04:14');
INSERT INTO `sms_orders` VALUES (5, 71, 32, 7, 3, '2020-12-11 09:25:17');
INSERT INTO `sms_orders` VALUES (5, 74, 33, 8, 7, '2020-12-11 09:26:11');
INSERT INTO `sms_orders` VALUES (6, 19, 38, 2.2, 5, '2020-05-07 00:05:00');
INSERT INTO `sms_orders` VALUES (6, 41, 34, 10, 6, '2020-11-11 09:26:38');
INSERT INTO `sms_orders` VALUES (6, 52, 35, 10, 6, '2020-11-11 09:27:20');
INSERT INTO `sms_orders` VALUES (7, 20, 38, 4.7, 2, '2020-06-11 00:05:46');
INSERT INTO `sms_orders` VALUES (7, 53, 32, 10, 7, '2020-12-11 09:30:19');
INSERT INTO `sms_orders` VALUES (8, 21, 33, 3.1, 3, '2020-07-11 00:06:17');
INSERT INTO `sms_orders` VALUES (8, 77, 38, 7, 10, '2020-01-11 09:39:04');
INSERT INTO `sms_orders` VALUES (9, 77, 38, 4.7, 20, '2020-02-11 09:39:22');
INSERT INTO `sms_orders` VALUES (10, 77, 38, 6.7, 30, '2020-05-11 09:39:54');
COMMIT;

-- ----------------------------
-- Table structure for sms_purchase
-- ----------------------------
DROP TABLE IF EXISTS `sms_purchase`;
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
  CONSTRAINT `sms_purchase_ibfk_2` FOREIGN KEY (`supplier_id`) REFERENCES `sms_suppliers` (`id`),
  CONSTRAINT `sms_purchase_chk_1` CHECK ((`if_finish` in (0,1))),
  CONSTRAINT `sms_purchase_chk_2` CHECK ((`if_shelf` in (0,1)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- ----------------------------
-- Records of sms_purchase
-- ----------------------------
BEGIN;
INSERT INTO `sms_purchase` VALUES (14, 32, '2020-01-11 00:09:41', '2020-01-13 00:09:48', 100, 2.5, 1, 1);
INSERT INTO `sms_purchase` VALUES (17, 38, '2020-03-11 00:10:36', '2020-03-21 00:10:46', 150, 3, 1, 1);
INSERT INTO `sms_purchase` VALUES (19, 33, '2020-04-11 00:11:21', '2020-05-11 00:11:30', 120, 2.1, 1, 1);
INSERT INTO `sms_purchase` VALUES (21, 34, '2020-02-11 00:12:18', '2021-02-15 00:12:29', 120, 35, 1, 1);
INSERT INTO `sms_purchase` VALUES (23, 35, '2020-01-21 00:13:59', '2020-01-30 00:14:10', 100, 23, 1, 1);
INSERT INTO `sms_purchase` VALUES (29, 36, '2020-03-11 00:16:02', '2020-04-11 00:16:14', 340, 5.7, 1, 1);
INSERT INTO `sms_purchase` VALUES (34, 38, '2020-05-11 00:16:51', '2020-06-11 00:17:02', 200, 2.3, 1, 1);
INSERT INTO `sms_purchase` VALUES (37, 39, '2021-06-11 00:18:07', '2020-07-16 00:18:14', 210, 3.2, 1, 1);
INSERT INTO `sms_purchase` VALUES (39, 39, '2020-08-01 00:19:47', '2020-08-31 00:20:09', 100, 7.8, 1, 1);
INSERT INTO `sms_purchase` VALUES (41, 35, '2020-09-01 00:22:51', '2020-09-21 00:23:04', 100, 3.2, 1, 1);
INSERT INTO `sms_purchase` VALUES (53, 32, '2020-10-11 00:23:43', '2020-10-30 00:23:58', 200, 2.5, 1, 1);
INSERT INTO `sms_purchase` VALUES (59, 33, '2020-11-11 00:24:36', '2020-12-11 00:24:46', 150, 2.3, 1, 0);
INSERT INTO `sms_purchase` VALUES (62, 34, '2020-12-11 00:25:24', '2021-01-11 00:26:03', 130, 4.7, 1, 1);
INSERT INTO `sms_purchase` VALUES (71, 33, '2021-01-11 00:30:14', '2021-01-20 00:30:19', 100, 4.5, 1, 1);
INSERT INTO `sms_purchase` VALUES (71, 35, '2020-12-31 00:26:28', '2021-01-21 00:26:38', 140, 5.2, 1, 1);
INSERT INTO `sms_purchase` VALUES (74, 38, '2021-01-11 00:27:22', '2021-01-21 00:27:30', 130, 6.7, 1, 1);
INSERT INTO `sms_purchase` VALUES (75, 34, '2020-01-01 00:28:18', '2021-01-11 00:28:24', 140, 6.5, 0, 0);
INSERT INTO `sms_purchase` VALUES (77, 38, '2020-01-01 09:33:27', '2020-01-11 09:33:35', 200, 3.2, 1, 1);
INSERT INTO `sms_purchase` VALUES (77, 38, '2020-02-11 09:34:19', '2020-03-11 09:34:24', 200, 4.5, 1, 1);
INSERT INTO `sms_purchase` VALUES (77, 38, '2020-03-11 09:34:56', '2020-04-11 09:35:06', 200, 3.8, 1, 1);
INSERT INTO `sms_purchase` VALUES (77, 38, '2020-04-11 09:35:30', '2020-05-11 09:35:40', 200, 5.7, 1, 1);
COMMIT;

-- ----------------------------
-- Table structure for sms_roles
-- ----------------------------
DROP TABLE IF EXISTS `sms_roles`;
CREATE TABLE `sms_roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- ----------------------------
-- Records of sms_roles
-- ----------------------------
BEGIN;
INSERT INTO `sms_roles` VALUES (2, 'admin');
INSERT INTO `sms_roles` VALUES (1, 'staff');
INSERT INTO `sms_roles` VALUES (3, 'superadmin');
COMMIT;

-- ----------------------------
-- Table structure for sms_sales
-- ----------------------------
DROP TABLE IF EXISTS `sms_sales`;
CREATE TABLE `sms_sales` (
  `good_id` int(11) NOT NULL,
  `supplier_id` int(11) NOT NULL,
  `price_out` float NOT NULL,
  `amount` float NOT NULL,
  PRIMARY KEY (`good_id`,`supplier_id`),
  KEY `supplier_id` (`supplier_id`),
  CONSTRAINT `sms_sales_ibfk_1` FOREIGN KEY (`good_id`) REFERENCES `sms_goods` (`id`),
  CONSTRAINT `sms_sales_ibfk_2` FOREIGN KEY (`supplier_id`) REFERENCES `sms_suppliers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- ----------------------------
-- Records of sms_sales
-- ----------------------------
BEGIN;
INSERT INTO `sms_sales` VALUES (37, 33, 12, 3);
COMMIT;

-- ----------------------------
-- Table structure for sms_stocks
-- ----------------------------
DROP TABLE IF EXISTS `sms_stocks`;
CREATE TABLE `sms_stocks` (
  `good_id` int(11) NOT NULL,
  `supplier_id` int(11) NOT NULL,
  `amount` float NOT NULL,
  PRIMARY KEY (`good_id`,`supplier_id`),
  KEY `supplier_id` (`supplier_id`),
  CONSTRAINT `sms_stocks_ibfk_1` FOREIGN KEY (`good_id`) REFERENCES `sms_goods` (`id`),
  CONSTRAINT `sms_stocks_ibfk_2` FOREIGN KEY (`supplier_id`) REFERENCES `sms_suppliers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- ----------------------------
-- Table structure for sms_suppliers
-- ----------------------------
DROP TABLE IF EXISTS `sms_suppliers`;
CREATE TABLE `sms_suppliers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `mobile` varchar(64) NOT NULL,
  `sign_start` date NOT NULL,
  `sign_end` date NOT NULL,
  `city` varchar(64) NOT NULL,
  `province` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- ----------------------------
-- Records of sms_suppliers
-- ----------------------------
BEGIN;
INSERT INTO `sms_suppliers` VALUES (32, '薯片大厂1234', '1234567', '2021-01-11', '2021-01-29', '朝阳区', '北京');
INSERT INTO `sms_suppliers` VALUES (33, '买家电的', '12345678999', '2021-01-11', '2021-01-03', '通辽市', '内蒙古');
INSERT INTO `sms_suppliers` VALUES (34, '宇宙第一美食厂', '12345678900', '2021-01-03', '2021-01-28', '朝阳区', '北京');
INSERT INTO `sms_suppliers` VALUES (35, '杂货商店', '12345678900', '2021-01-05', '2021-01-13', '外滩', '上海');
INSERT INTO `sms_suppliers` VALUES (36, '好多能用的厂', '13345678900', '2020-01-01', '2021-01-30', '朝阳区', '北京');
INSERT INTO `sms_suppliers` VALUES (38, '卖生鲜水果的', '12345678900', '2021-01-01', '2021-01-02', '安顺市', '贵州');
INSERT INTO `sms_suppliers` VALUES (39, '智能电器', '13456789090', '2021-01-01', '2021-01-02', '朝阳区', '北京');
INSERT INTO `sms_suppliers` VALUES (40, '阿巴巴', '1234567', '2021-01-11', '2022-02-06', '宁波市', '浙江');
INSERT INTO `sms_suppliers` VALUES (41, '黄金时代分工表', '1234567', '2021-01-06', '2021-01-28', '嘉兴市', '浙江');
INSERT INTO `sms_suppliers` VALUES (42, 'HBZsgvdf\'', '12345678', '2021-01-12', '2021-02-05', '河东区', '天津');
INSERT INTO `sms_suppliers` VALUES (43, '天府之国', '12345678900', '2021-01-11', '2021-01-31', '成都市', '四川');
INSERT INTO `sms_suppliers` VALUES (44, '哈哈哈哈哈', '12345678900', '2021-01-13', '2021-01-29', '朝阳区', '北京');
INSERT INTO `sms_suppliers` VALUES (45, 'ceshi', '12345678900', '2021-01-04', '2021-01-08', '朝阳区', '北京');
INSERT INTO `sms_suppliers` VALUES (47, 'bug', '13456789000', '2021-01-01', '2021-01-29', '朝阳区', '北京');
INSERT INTO `sms_suppliers` VALUES (49, 'xinjiang', '13456789000', '2021-01-01', '2021-01-29', '乌鲁木齐市', '新疆');
INSERT INTO `sms_suppliers` VALUES (50, 'test', '1234567', '2021-01-05', '2021-01-29', '拉萨市', '西藏');
COMMIT;

-- ----------------------------
-- Table structure for sms_users
-- ----------------------------
DROP TABLE IF EXISTS `sms_users`;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- ----------------------------
-- Records of sms_users
-- ----------------------------
BEGIN;
INSERT INTO `sms_users` VALUES ('1234567', '', 'zhong', '男', '2000-06-20', '13456789000', '山西,大同市,城区', 5000, 1);
INSERT INTO `sms_users` VALUES ('2017040300', '1234589000', '王小虎', '男', '2021-01-10', '13754546789', '湖北,宜昌市,猇亭区', 5000, 3);
INSERT INTO `sms_users` VALUES ('2017040380', '2017040380', '石雯雯', '女', '2000-06-22', '18810275361', '北京,东城区', 5000, 3);
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
