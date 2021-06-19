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

 Date: 16/06/2021 14:09:00
*/
CREATE DATABASE IF NOT EXISTS infos;
USE infos;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for province_info
-- ----------------------------
DROP TABLE IF EXISTS `province_info`;
CREATE TABLE `province_info` (
  `country_name` varchar(20) DEFAULT NULL,
  `province_name` varchar(20) DEFAULT NULL UNIQUE,
  `currentConfirmedCount` int DEFAULT NULL,
  `suspectedCount` int DEFAULT NULL,
  `curedCount` int DEFAULT NULL,
  `deadCount` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

SET FOREIGN_KEY_CHECKS = 1;
