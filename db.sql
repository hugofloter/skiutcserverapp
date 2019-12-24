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


--
-- Table structure for table `potin`
--

ALTER TABLE `users_app` DROP PRIMARY KEY, ADD PRIMARY KEY (`login`);

CREATE TABLE IF NOT EXISTS `potin` (
  `id` int(10) PRIMARY KEY AUTO_INCREMENT,
  `title` varchar(20),
  `text` text,
  `approved` boolean DEFAULT FALSE,
  `sender` varchar(40) NOT NULL,
  `isAnonymous` boolean DEFAULT TRUE,
  INDEX sender_index (sender),
  FOREIGN KEY (sender)
    REFERENCES users_app(login)
    ON DELETE CASCADE
);

--
-- Udpate table potin
--
ALTER TABLE `potin` MODIFY  `title` VARCHAR(50);


--
-- Update table user
--
ALTER TABLE `users_app` DROP `isAdmin`, ADD `isAdmin` Boolean DEFAULT 0;
ALTER TABLE `users_app` DROP `lastPosition`, ADD `lastPosition` varchar(30) DEFAULT NULL;
ALTER TABLE `users_app` MODIFY `email` VARCHAR(50);