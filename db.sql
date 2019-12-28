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
  `login` varchar(40) PRIMARY KEY,
  `lastname` varchar(40) DEFAULT NULL,
  `firstname` varchar(40) DEFAULT NULL,
  `email` varchar(40) DEFAULT NULL,
  `password` varbinary(50) DEFAULT NULL,
  `isAdmin` Boolean DEFAULT FALSE,
  `lastPosition` varchar(30) DEFAULT NULL
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

--
-- Table structure for table `groups`
--

CREATE TABLE IF NOT EXISTS `groups` (
  `id` int(10) PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(20),
  `owner` varchar(40) NOT NULL,
  `beer_call` date DEFAULT NULL,
  INDEX owner_index (owner),
  FOREIGN KEY (owner)
    REFERENCES users_app(login)
    ON DELETE CASCADE
);

--
-- Table structure for table `usergroup`
--

CREATE TABLE IF NOT EXISTS `usergroup` (
  `login_user` varchar(20) NOT NULL,
  `id_group` int(10) NOT NULL,
  `status` ENUM('V', 'P') DEFAULT 'P',
  `share_position` boolean DEFAULT FALSE,
  `expiration_date` date DEFAULT NULL,
  INDEX group_index (id_group),
  FOREIGN KEY (id_group)
    REFERENCES `groups`(id)
    ON DELETE CASCADE
);