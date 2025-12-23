-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: quan_ly_nha_hang
-- ------------------------------------------------------
-- Server version	8.0.42

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
-- Table structure for table `banan`
--

DROP TABLE IF EXISTS `banan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `banan` (
  `SoBan` int NOT NULL,
  `TrangThai` enum('Trong','CoKhach','DatTruoc') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'Trong',
  `Tang` int DEFAULT '1',
  `SoGhe` int DEFAULT '4',
  PRIMARY KEY (`SoBan`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `banan`
--

LOCK TABLES `banan` WRITE;
/*!40000 ALTER TABLE `banan` DISABLE KEYS */;
INSERT INTO `banan` VALUES (1,'Trong',1,4),(2,'Trong',1,4),(3,'CoKhach',1,4),(4,'Trong',1,4),(5,'Trong',1,4),(6,'Trong',1,4),(7,'Trong',1,4),(8,'Trong',1,4),(9,'Trong',1,8),(10,'DatTruoc',1,8),(11,'Trong',2,4),(12,'Trong',2,4),(13,'Trong',2,4),(14,'Trong',2,4),(15,'Trong',2,4),(16,'Trong',2,4),(17,'Trong',2,4),(18,'Trong',2,4),(19,'Trong',2,8),(20,'Trong',2,8);
/*!40000 ALTER TABLE `banan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chitiethoadon`
--

DROP TABLE IF EXISTS `chitiethoadon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chitiethoadon` (
  `MaChiTiet` int NOT NULL AUTO_INCREMENT,
  `MaHoaDon` int NOT NULL,
  `MaMon` int NOT NULL,
  `SoLuong` int DEFAULT '1',
  `DonGia` decimal(10,0) NOT NULL,
  `TrangThaiMon` enum('ChoCheBien','DangCheBien','HoanTat','DaHuy','Served') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'ChoCheBien',
  `ThoiGianGoi` datetime DEFAULT CURRENT_TIMESTAMP,
  `GhiChu` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`MaChiTiet`),
  KEY `MaHoaDon` (`MaHoaDon`),
  KEY `MaMon` (`MaMon`),
  CONSTRAINT `chitiethoadon_ibfk_1` FOREIGN KEY (`MaHoaDon`) REFERENCES `hoadon` (`MaHoaDon`),
  CONSTRAINT `chitiethoadon_ibfk_2` FOREIGN KEY (`MaMon`) REFERENCES `monan` (`MaMon`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chitiethoadon`
--

LOCK TABLES `chitiethoadon` WRITE;
/*!40000 ALTER TABLE `chitiethoadon` DISABLE KEYS */;
INSERT INTO `chitiethoadon` VALUES (1,1,2,2,42000,'ChoCheBien','2025-12-23 23:41:04',NULL),(2,1,11,1,55000,'ChoCheBien','2025-12-23 23:41:04',NULL);
/*!40000 ALTER TABLE `chitiethoadon` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chitietphieugoi`
--

DROP TABLE IF EXISTS `chitietphieugoi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chitietphieugoi` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `MaPhieu` int NOT NULL,
  `MaMon` int NOT NULL,
  `SoLuong` int NOT NULL,
  `GhiChu` varchar(45) DEFAULT NULL,
  `TrangThai` enum('ChoCheBien','DangCheBien','HoanTat','DaPhucVu') DEFAULT 'ChoCheBien',
  PRIMARY KEY (`ID`),
  KEY `MaPhieu_idx` (`MaPhieu`),
  KEY `MaMon_idx` (`MaMon`),
  CONSTRAINT `MaMon` FOREIGN KEY (`MaMon`) REFERENCES `monan` (`MaMon`),
  CONSTRAINT `MaPhieu` FOREIGN KEY (`MaPhieu`) REFERENCES `phieugoi` (`MaPhieu`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chitietphieugoi`
--

LOCK TABLES `chitietphieugoi` WRITE;
/*!40000 ALTER TABLE `chitietphieugoi` DISABLE KEYS */;
INSERT INTO `chitietphieugoi` VALUES (1,1,2,2,'','DaPhucVu'),(2,1,11,1,'','DaPhucVu');
/*!40000 ALTER TABLE `chitietphieugoi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hoadon`
--

DROP TABLE IF EXISTS `hoadon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hoadon` (
  `MaHoaDon` int NOT NULL AUTO_INCREMENT,
  `SoBan` int NOT NULL,
  `MaNV_PhucVu` int DEFAULT NULL,
  `ThoiGianVao` datetime DEFAULT CURRENT_TIMESTAMP,
  `ThoiGianRa` datetime DEFAULT NULL,
  `TongThanhToan` decimal(10,0) DEFAULT '0',
  `TongTienHang` decimal(10,0) DEFAULT '0',
  `GiamGia` decimal(10,0) DEFAULT '0',
  `VAT` decimal(10,0) DEFAULT '0',
  `TrangThai` enum('ChuaThanhToan','DaThanhToan') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'ChuaThanhToan',
  `GhiChu` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `TienKhachDua` decimal(10,0) DEFAULT '0',
  `TienThua` decimal(10,0) DEFAULT '0',
  PRIMARY KEY (`MaHoaDon`),
  KEY `SoBan` (`SoBan`),
  KEY `MaNV_PhucVu` (`MaNV_PhucVu`),
  CONSTRAINT `hoadon_ibfk_1` FOREIGN KEY (`SoBan`) REFERENCES `banan` (`SoBan`),
  CONSTRAINT `hoadon_ibfk_2` FOREIGN KEY (`MaNV_PhucVu`) REFERENCES `nhanvien` (`MaNV`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hoadon`
--

LOCK TABLES `hoadon` WRITE;
/*!40000 ALTER TABLE `hoadon` DISABLE KEYS */;
INSERT INTO `hoadon` VALUES (1,1,NULL,'2025-12-23 23:41:04','2025-12-23 23:42:03',152900,0,0,0,'DaThanhToan',NULL,200000,47100);
/*!40000 ALTER TABLE `hoadon` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `monan`
--

DROP TABLE IF EXISTS `monan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `monan` (
  `MaMon` int NOT NULL AUTO_INCREMENT,
  `MaCode` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `TenMon` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `DonVi` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `GiaTien` decimal(10,0) NOT NULL,
  `MaNhom` int DEFAULT NULL,
  `HinhAnh` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `DangKinhDoanh` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`MaMon`),
  KEY `MaNhom` (`MaNhom`),
  CONSTRAINT `monan_ibfk_1` FOREIGN KEY (`MaNhom`) REFERENCES `nhommon` (`MaNhom`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `monan`
--

LOCK TABLES `monan` WRITE;
/*!40000 ALTER TABLE `monan` DISABLE KEYS */;
INSERT INTO `monan` VALUES (1,'COM01','Cơm cà ri',NULL,45000,1,'https://res.cloudinary.com/dschg4bcn/image/upload/w_500,h_500,c_fill/v1763990917/c%C6%A1m_c%C3%A0_ri_ti0pkf.png',1),(2,'COM02','Cơm bulgogi',NULL,42000,1,'https://res.cloudinary.com/dschg4bcn/image/upload/w_500,h_500,c_fill/v1763990915/c%C6%A1m_bulgogi_hfvtjo.png',1),(3,'COM03','Cơm cá ngừ',NULL,45000,1,'https://res.cloudinary.com/dschg4bcn/image/upload/w_500,h_500,c_fill/v1763990914/c%C6%A1m_c%C3%A1_ng%E1%BB%AB_vthndp.png',1),(4,'COM04','Cơm bibimbap',NULL,40000,1,'https://res.cloudinary.com/dschg4bcn/image/upload/w_500,h_500,c_fill/v1763990914/c%C6%A1m_bibimbap_eqek7f.png',1),(5,'KB01','Kimbap',NULL,40000,1,'https://res.cloudinary.com/dschg4bcn/image/upload/w_500,h_500,c_fill/v1763990923/kimbap_fxdkfk.png',1),(6,'COM05','Cơm gà cay',NULL,54000,1,'https://res.cloudinary.com/dschg4bcn/image/upload/w_500,h_500,c_fill/v1763990913/c%C6%A1m_g%C3%A0_cay_eidmfh.png',1),(7,'MI01','Kim chi ramen',NULL,39000,2,'https://res.cloudinary.com/dschg4bcn/image/upload/w_500,h_500,c_fill/v1763989961/kimchi_ramen_pnzldp.png',1),(8,'TOK01','Tokbokki ramen',NULL,35000,2,'https://res.cloudinary.com/dschg4bcn/image/upload/w_500,h_500,c_fill/v1763989960/tok_ramen_pkjpzw.png',1),(9,'TOK02','Tokbokki phô mai',NULL,30000,2,'https://res.cloudinary.com/dschg4bcn/image/upload/w_500,h_500,c_fill/v1763989954/tok_ph%C3%B4_mai_fuefxw.png',1),(10,'TOK03','Tokbokki cay',NULL,30000,2,'https://res.cloudinary.com/dschg4bcn/image/upload/w_500,h_500,c_fill/v1763989955/tok_cay_l4cgpg.png',1),(11,'GA01','Gà cay ngọt',NULL,55000,3,'https://res.cloudinary.com/dschg4bcn/image/upload/w_500,h_500,c_fill/v1763991323/g%C3%A0_cay_ng%E1%BB%8Dt_ozekrv.png',1),(12,'CB01','Cheeseball',NULL,40000,3,'https://res.cloudinary.com/dschg4bcn/image/upload/w_500,h_500,c_fill/v1764170825/z7265877736300_c45f8e1f05cde40b6f4e33748e4e5add_weuqmc.jpg',1),(13,'GA03','Gà chua cay',NULL,55000,3,'https://res.cloudinary.com/dschg4bcn/image/upload/w_500,h_500,c_fill/v1763991322/g%C3%A0_chua_cay_cl5o9b.png',1),(14,'HEO01','Thịt heo nướng',NULL,68000,3,'https://res.cloudinary.com/dschg4bcn/image/upload/w_500,h_500,c_fill/v1764170825/thitheonuong_qwq4e3.jpg',1),(15,'GA05','Gà sốt bơ tỏi',NULL,55000,3,'https://res.cloudinary.com/dschg4bcn/image/upload/w_500,h_500,c_fill/v1763991320/g%C3%A0_s%E1%BB%91t_b%C6%A1_t%E1%BB%8Fi_habyh1.png',1),(16,'GA06','Gà sốt mật ong',NULL,55000,3,'https://res.cloudinary.com/dschg4bcn/image/upload/w_500,h_500,c_fill/v1763991318/g%C3%A0_s%E1%BB%91t_m%E1%BA%ADt_ong_bjt9xn.png',1),(17,'LAU01','Lẩu bulgogi',NULL,57000,4,'https://res.cloudinary.com/dschg4bcn/image/upload/w_500,h_500,c_fill/v1763991456/l%E1%BA%A9u_bulgogi_mofjeh.png',1),(18,'LAU02','Lẩu kim chi',NULL,57000,4,'https://res.cloudinary.com/dschg4bcn/image/upload/w_500,h_500,c_fill/v1763991524/l%E1%BA%A9u_kimchi_svs7se.png',1),(19,'DR01','Pepsi','Lon',13000,5,'https://res.cloudinary.com/dschg4bcn/image/upload/w_500,h_500,c_fill/v1763990146/pepsi_uqfl3w.png',1),(20,'DR02','Mirinda','Lon',13000,5,'https://res.cloudinary.com/dschg4bcn/image/upload/w_500,h_500,c_fill/v1763990145/mirinda_ipenxx.png',1),(21,'DR03','7UP','Lon',13000,5,'https://res.cloudinary.com/dschg4bcn/image/upload/w_500,h_500,c_fill/v1763990144/7up_dwua53.png',1),(22,'DR04','Trà vải','Ly',28000,5,'https://res.cloudinary.com/dschg4bcn/image/upload/w_500,h_500,c_fill/v1763990144/tr%C3%A0_v%E1%BA%A3i_wdhay9.png',1),(23,'DR05','Olong tắc','Ly',25000,5,'https://res.cloudinary.com/dschg4bcn/image/upload/w_500,h_500,c_fill/v1763990145/olong_t%E1%BA%AFc_frycog.png',1),(24,'DR06','Trà đào','Ly',30000,5,'https://res.cloudinary.com/dschg4bcn/image/upload/w_500,h_500,c_fill/v1763990143/tr%C3%A0_%C4%91%C3%A0o_zbgxtm.png',1),(25,'DR07','Soda Việt Quất','Ly',29000,5,'https://res.cloudinary.com/dschg4bcn/image/upload/w_500,h_500,c_fill/v1763990142/soda_vi%E1%BB%87t_qu%E1%BA%A5t_n6cq3s.png',1),(26,'DR08','Soda Nho','Ly',29000,5,'https://res.cloudinary.com/dschg4bcn/image/upload/w_500,h_500,c_fill/v1763990142/soda_nho_dmryjn.png',1),(27,'DR09','Soda dưa lưới','Ly',29000,5,'https://res.cloudinary.com/dschg4bcn/image/upload/w_500,h_500,c_fill/v1763990142/soda_d%C6%B0a_l%C6%B0%E1%BB%9Bi_hf5ivn.png',1),(28,'ADD01','Cơm thêm','Chén',5000,6,'https://res.cloudinary.com/dschg4bcn/image/upload/w_500,h_500,c_fill/v1763991142/c%C6%A1m_th%C3%AAm_swupqt.png',1),(29,'ADD02','Trứng gà','Quả',5000,6,'https://res.cloudinary.com/dschg4bcn/image/upload/w_500,h_500,c_fill/v1763991139/tr%E1%BB%A9ng_g%C3%A0_ar8nhl.png',1),(30,'ADD03','Mandu','Cái',8000,6,'https://res.cloudinary.com/dschg4bcn/image/upload/w_500,h_500,c_fill/v1763991140/mandu_nocr7v.png',1),(31,'ADD04','Chả cá','Xiên',15000,6,'https://res.cloudinary.com/dschg4bcn/image/upload/w_500,h_500,c_fill/v1763991136/ch%E1%BA%A3_c%C3%A1_omgfge.png',1),(32,'ADD05','Bánh gạo','Phần',2000,6,'https://res.cloudinary.com/dschg4bcn/image/upload/w_500,h_500,c_fill/v1763991135/b%C3%A1nh_g%E1%BA%A1o_xln5st.png',1),(33,'SOT01','Sốt chua cay','Chén',6000,6,'https://res.cloudinary.com/dschg4bcn/image/upload/v1763991133/s%E1%BB%91t_chua_cay_bftctb.png',1),(34,'SOT02','Sốt cay ngọt','Chén',6000,6,'https://res.cloudinary.com/dschg4bcn/image/upload/v1763991135/s%E1%BB%91t_cay_ng%E1%BB%8Dt_kzduo4.png',1),(35,'SOT03','Sốt Mayo','Chén',6000,6,'https://res.cloudinary.com/dschg4bcn/image/upload/v1763991134/s%E1%BB%91t_mayo_zxf4dy.png',1);
/*!40000 ALTER TABLE `monan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nhanvien`
--

DROP TABLE IF EXISTS `nhanvien`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nhanvien` (
  `MaNV` int NOT NULL AUTO_INCREMENT,
  `TenDangNhap` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `MatKhau` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `HoTen` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `VaiTro` enum('Admin','QuanLy','PhucVu','Bep','ThuNgan') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `NgayTao` datetime DEFAULT CURRENT_TIMESTAMP,
  `Avatar` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`MaNV`),
  UNIQUE KEY `TenDangNhap` (`TenDangNhap`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nhanvien`
--

LOCK TABLES `nhanvien` WRITE;
/*!40000 ALTER TABLE `nhanvien` DISABLE KEYS */;
INSERT INTO `nhanvien` VALUES (1,'admin','123','Admin Hệ Thống','Admin','2025-11-27 21:38:40','https://res.cloudinary.com/dschg4bcn/image/upload/v1764867303/avatar-admin_xfsnxv.webp'),(2,'manager','123','Nguyễn Quản Lý','QuanLy','2025-11-27 21:38:40','https://res.cloudinary.com/dschg4bcn/image/upload/v1764867304/avatar-manager_mreqrv.avif'),(3,'pv01','123','Phục Vụ 1','PhucVu','2025-11-27 21:38:40','https://res.cloudinary.com/dschg4bcn/image/upload/v1764867304/avatar-pv_thao2i.webp'),(4,'pv02','123','Phục Vụ 2','PhucVu','2025-11-27 21:38:40','https://res.cloudinary.com/dschg4bcn/image/upload/v1764867304/avatar-pv_thao2i.webp'),(5,'pv03','123','Phục Vụ 3','PhucVu','2025-11-27 21:38:40','https://res.cloudinary.com/dschg4bcn/image/upload/v1764867304/avatar-pv_thao2i.webp'),(6,'pv04','123','Phục Vụ 4','PhucVu','2025-11-27 21:38:40','https://res.cloudinary.com/dschg4bcn/image/upload/v1764867304/avatar-pv_thao2i.webp'),(7,'pv05','123','Phục Vụ 5','PhucVu','2025-11-27 21:38:40','https://res.cloudinary.com/dschg4bcn/image/upload/v1764867304/avatar-pv_thao2i.webp'),(8,'bep01','123','Đầu bếp 1','Bep','2025-11-27 21:38:40','https://res.cloudinary.com/dschg4bcn/image/upload/v1764867304/avatar-bep_u3jbhb.webp'),(9,'bep02','123','Đầu bếp 2','Bep','2025-11-27 21:38:40','https://res.cloudinary.com/dschg4bcn/image/upload/v1764867304/avatar-bep_u3jbhb.webp'),(10,'bep03','123','Đầu bếp 3','Bep','2025-11-27 21:38:40','https://res.cloudinary.com/dschg4bcn/image/upload/v1764867304/avatar-bep_u3jbhb.webp'),(11,'bep04','123','Đầu bếp 4','Bep','2025-11-27 21:38:40','https://res.cloudinary.com/dschg4bcn/image/upload/v1764867304/avatar-bep_u3jbhb.webp'),(12,'bep05','123','Đầu bếp 5','Bep','2025-11-27 21:38:40','https://res.cloudinary.com/dschg4bcn/image/upload/v1764867304/avatar-bep_u3jbhb.webp'),(13,'tn01','123','Thu Ngân 1','ThuNgan','2025-11-27 21:38:40','https://res.cloudinary.com/dschg4bcn/image/upload/v1764867304/avatar-tn_mxug5u.webp'),(14,'tn02','123','Thu Ngân 2','ThuNgan','2025-11-27 21:38:40','https://res.cloudinary.com/dschg4bcn/image/upload/v1764867304/avatar-tn_mxug5u.webp'),(15,'tn03','123','Thu Ngân 3','ThuNgan','2025-11-27 21:38:40','https://res.cloudinary.com/dschg4bcn/image/upload/v1764867304/avatar-tn_mxug5u.webp');
/*!40000 ALTER TABLE `nhanvien` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nhommon`
--

DROP TABLE IF EXISTS `nhommon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nhommon` (
  `MaNhom` int NOT NULL AUTO_INCREMENT,
  `TenNhom` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`MaNhom`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nhommon`
--

LOCK TABLES `nhommon` WRITE;
/*!40000 ALTER TABLE `nhommon` DISABLE KEYS */;
INSERT INTO `nhommon` VALUES (1,'Món Cơm'),(2,'Món Mì & Tokbokki'),(3,'Món Gà'),(4,'Món Lẩu'),(5,'Đồ Uống'),(6,'Món Thêm');
/*!40000 ALTER TABLE `nhommon` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `phieugoi`
--

DROP TABLE IF EXISTS `phieugoi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `phieugoi` (
  `MaPhieu` int NOT NULL AUTO_INCREMENT,
  `MaHoaDon` int NOT NULL,
  `ThoiGianTao` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`MaPhieu`),
  KEY `MaHoaDon_idx` (`MaHoaDon`),
  CONSTRAINT `MaHoaDon` FOREIGN KEY (`MaHoaDon`) REFERENCES `hoadon` (`MaHoaDon`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `phieugoi`
--

LOCK TABLES `phieugoi` WRITE;
/*!40000 ALTER TABLE `phieugoi` DISABLE KEYS */;
INSERT INTO `phieugoi` VALUES (1,1,'2025-12-23 23:41:04');
/*!40000 ALTER TABLE `phieugoi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `thongbao`
--

DROP TABLE IF EXISTS `thongbao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `thongbao` (
  `MaTB` int NOT NULL AUTO_INCREMENT,
  `NoiDung` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `DaXem` tinyint(1) DEFAULT '0',
  `ThoiGian` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`MaTB`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `thongbao`
--

LOCK TABLES `thongbao` WRITE;
/*!40000 ALTER TABLE `thongbao` DISABLE KEYS */;
INSERT INTO `thongbao` VALUES (1,'Bàn 1: Gà cay ngọt đã nấu xong!',0,'2025-12-23 23:41:24'),(2,'Bàn 1: Cơm bulgogi đã nấu xong!',0,'2025-12-23 23:41:24');
/*!40000 ALTER TABLE `thongbao` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-23 23:43:30
