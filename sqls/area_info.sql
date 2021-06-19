/*
 Navicat Premium Data Transfer

 Source Server         : mysqlconn
 Source Server Type    : MySQL
 Source Server Version : 80025
 Source Host           : 127.0.0.1:3306
 Source Schema         : infos

 Target Server Type    : MySQL
 Target Server Version : 80025
 File Encoding         : 65001

 Date: 16/06/2021 14:02:34
*/

CREATE DATABASE IF NOT EXISTS infos;
USE infos;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for area_info
-- ----------------------------
DROP TABLE IF EXISTS `area_info`;
CREATE TABLE `area_info` (
  `provinceName` varchar(20) DEFAULT NULL unique,
  `currentConfirmedCount` int DEFAULT NULL,
  `confirmedCount` int DEFAULT NULL,
  `suspectedCount` int DEFAULT NULL,
  `curedCount` int DEFAULT NULL,
  `deadCount` int DEFAULT NULL,
  `highDangerCount` int DEFAULT NULL,
  `midDangerCount` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

SET FOREIGN_KEY_CHECKS = 1;
