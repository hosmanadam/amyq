CREATE DATABASE  IF NOT EXISTS `amyq_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */;
USE `amyq_db`;
-- MySQL dump 10.13  Distrib 8.0.13, for macos10.14 (x86_64)
--
-- Host: 127.0.0.1    Database: amyq_db
-- ------------------------------------------------------
-- Server version	8.0.13

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `answers`
--

DROP TABLE IF EXISTS `answers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `answers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question_id` int(11) NOT NULL,
  `vote_count` int(11) NOT NULL DEFAULT '0',
  `body` varchar(1000) NOT NULL,
  `image_url` varchar(100) DEFAULT NULL,
  `time_submitted` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `question_id` (`question_id`),
  CONSTRAINT `answers_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `questions` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `answers`
--

LOCK TABLES `answers` WRITE;
/*!40000 ALTER TABLE `answers` DISABLE KEYS */;
INSERT INTO `answers` VALUES (1,1,3,'42,  you dummy',NULL,'2010-10-10 11:11:11'),(2,1,4,'42 like the other guy says',NULL,'2011-10-10 12:11:11'),(3,2,4,'cause its not red',NULL,'2012-10-10 13:11:11'),(4,2,5,'The athmospheroic space has only very small holes in it. So when all the colors come in sunlight, the holes only let blue color through because it\'s the smallest color.',NULL,'2019-01-27 16:29:36'),(5,4,0,'Yep, mine is old now, you can have it for a bag of flour. Email me at missjane@gmail.com!',NULL,'2019-01-27 16:39:52'),(6,3,0,'It\'s probably genetic.',NULL,'2019-01-27 16:41:43'),(7,5,1,'You\'re just super unlucky I guess!',NULL,'2019-01-27 16:51:06'),(8,5,2,'Have you tried sexy underwear?',NULL,'2019-01-27 16:51:21'),(9,6,-2,'It was invented in the stone age, do you know how dirty they were back then? No wonder its disgusting LOL',NULL,'2019-01-27 17:00:48'),(10,7,0,'No.          ',NULL,'2019-01-27 17:04:06'),(11,6,5,'You don\'t know what you\'re talking about.',NULL,'2019-01-27 17:14:58'),(12,8,5,'They\'re too busy counting their money, no time to serve your HTTP requests LOL','https://www.kiplinger.com/kipimages/ledes/smart-ways-to-spend-1K-373x261.jpg','2019-01-27 17:20:51'),(13,9,0,'It\'s a well-known fact in the world of marketing that black is the coolest color.\r\nSo when poor people trample each other to death to get the last TV for 50% off, they can feel cool because they\'re participating in BLACK Friday!',NULL,'2019-01-27 17:25:10'),(14,10,-6,'Justin Bieber is not a band, he\'s a singer. The coolest band is Britney Spears.',NULL,'2019-01-27 17:29:13'),(15,11,1,'It used to be Mr. Bill Gates but then Windows XP crashed and not anymore.',NULL,'2019-01-27 19:00:44');
/*!40000 ALTER TABLE `answers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question_id` int(11) DEFAULT NULL,
  `answer_id` int(11) DEFAULT NULL,
  `body` varchar(1000) DEFAULT NULL,
  `time_submitted` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `question_id` (`question_id`),
  KEY `answer_id` (`answer_id`),
  CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `questions` (`id`) ON DELETE CASCADE,
  CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`answer_id`) REFERENCES `answers` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
INSERT INTO `comments` VALUES (1,NULL,1,'please dont be so rude','2010-10-10 11:11:11'),(2,NULL,3,'Haha, very clever.','2019-01-27 16:26:58'),(3,NULL,3,'Yeah, that\'s totally not helpful!!!','2019-01-27 16:27:19'),(4,NULL,4,'Sounds valid to me!','2019-01-27 16:30:30'),(5,4,NULL,'Why would anyone who has a kitten sell it? It\'s the best thing you can have.','2019-01-27 16:38:43'),(6,NULL,5,'OMG your heartlessness is so big I can\'t even!','2019-01-27 16:40:11'),(7,NULL,6,'I agree, and so would Darwin!','2019-01-27 16:42:05'),(8,NULL,6,'Darwin sucks, I prefer God.','2019-01-27 16:42:19'),(9,NULL,6,'Truth is not a matter of preference my friend!','2019-01-27 16:43:20'),(10,NULL,8,'Yep, that always works for me!','2019-01-27 16:51:43'),(11,NULL,10,'C\'mon, no need to be rude... He\'s trying his wings, a couple more comments like yours and he\'ll be single forever!','2019-01-27 17:04:57'),(12,8,NULL,'Have you tried restarting it?','2019-01-27 17:19:50'),(13,NULL,13,'Yep, I\'ve read that study as well!','2019-01-27 17:27:08'),(14,11,NULL,'I like that you corrected the \'man\' part and apologized. Shows character.','2019-01-27 18:59:52');
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `questions`
--

DROP TABLE IF EXISTS `questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `questions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `view_count` int(11) NOT NULL DEFAULT '0',
  `vote_count` int(11) NOT NULL DEFAULT '0',
  `title` varchar(100) NOT NULL,
  `body` varchar(1000) DEFAULT NULL,
  `image_url` varchar(1000) DEFAULT NULL,
  `time_submitted` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `questions`
--

LOCK TABLES `questions` WRITE;
/*!40000 ALTER TABLE `questions` DISABLE KEYS */;
INSERT INTO `questions` VALUES (1,3,3,'Whats the meaning of life?','Ive wondered about this since I was a kid, please let me know ASAP',NULL,'2011-10-09 12:11:11'),(2,4,4,'Why is the sky blue?','I wont be able to sleep until you answer, please help!!!','https://images.pexels.com/photos/912110/pexels-photo-912110.jpeg','2012-10-09 13:11:11'),(3,2,4,'How is she so cute???','Seriously!!!!!!','https://www.petmd.com/sites/default/files/petmd-kitten-development.jpg','2013-10-09 13:11:11'),(4,0,0,'Wanna buy cat','Anyone has a kitten for sale?',NULL,'2019-01-27 16:38:11'),(5,0,-3,'Why am I in love with the wrong person?','We\'ve been dating for 2 years with this guy I\'m crazy about and he still refuses to buy me my own house. I\'m really hot, so I don\'t understand why! Pls help!',NULL,'2019-01-27 16:50:24'),(6,0,-1,'Why is beer so gross?',NULL,'https://mir-s3-cdn-cf.behance.net/project_modules/max_1200/f8c78936499599.571edcc901c64.jpg','2019-01-27 16:58:40'),(7,0,0,'wanna chat?','Boy, 16',NULL,'2019-01-27 17:02:55'),(8,0,2,'Why is Facebook so slow?','I\'ts like literally not-responsive at all!!!',NULL,'2019-01-27 17:19:21'),(9,1,0,'Why is it \"Black Friday\"?','Why not white or something else?',NULL,'2019-01-27 17:23:28'),(10,0,0,'What\'s the coolest band?','I\'m thinking Justin Bieber, but I\'m not sure (only 13)',NULL,'2019-01-27 17:28:41'),(11,2,0,'Who\'s the richest man in the world?','I mean the richest person, sorry.',NULL,'2019-01-27 18:59:10');
/*!40000 ALTER TABLE `questions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tags`
--

DROP TABLE IF EXISTS `tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL UNIQUE,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tags`
--

LOCK TABLES `tags` WRITE;
/*!40000 ALTER TABLE `tags` DISABLE KEYS */;
INSERT INTO `tags` VALUES (1,'meaningoflife'),(2,'naturessecrets'),(3,'colorsareawesome');
/*!40000 ALTER TABLE `tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tags_to_questions`
--

DROP TABLE IF EXISTS `tags_to_questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `tags_to_questions` (
  `question_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  KEY `question_id` (`question_id`),
  KEY `tag_id` (`tag_id`),
  CONSTRAINT `tags_to_questions_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `questions` (`id`) ON DELETE CASCADE,
  CONSTRAINT `tags_to_questions_ibfk_2` FOREIGN KEY (`tag_id`) REFERENCES `tags` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tags_to_questions`
--

LOCK TABLES `tags_to_questions` WRITE;
/*!40000 ALTER TABLE `tags_to_questions` DISABLE KEYS */;
INSERT INTO `tags_to_questions` VALUES (1,1),(2,2),(2,3);
/*!40000 ALTER TABLE `tags_to_questions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-01-27 22:08:16
