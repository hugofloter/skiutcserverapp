--
-- Table structure for table `auth_token`
--
CREATE DATABASE IF NOT EXISTS skiutcapp;

USE skiutcapp;

CREATE TABLE IF NOT EXISTS `auth_token` (
  `login` varchar(40) NOT NULL,
  `token` varchar(50) DEFAULT NULL,
  UNIQUE KEY `login` (`login`)
);


--
-- Table structure for table `users_app`
--
CREATE TABLE IF NOT EXISTS`users_app` (
  `login` varchar(40) DEFAULT NULL,
  `lastname` varchar(40) DEFAULT NULL,
  `firstname` varchar(40) DEFAULT NULL,
  `email` varchar(40) DEFAULT NULL,
  `password` varbinary(50) DEFAULT NULL
);

--
-- Table structure for table `news`
--

CREATE TABLE IF NOT EXISTS `news` (
  `id` int(10) PRIMARY KEY AUTO_INCREMENT,
  `title` varchar(20),
  `text` text,
  `photo` varchar(100) DEFAULT NULL,
  `date` DATETIME,
  `type` ENUM('news', 'email')
);
