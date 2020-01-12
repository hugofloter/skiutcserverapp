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
  `email` varchar(50) DEFAULT NULL,
  `isAdmin` Boolean DEFAULT FALSE,
  `lastPosition` POINT DEFAULT NULL, #Changement of type
  `password` varbinary(50) DEFAULT NULL,
  `push_token` varchar(250) DEFAULT NULL,
  `img_url` varchar(100) DEFAULT NULL,
  `img_width` int(10) DEFAULT NULL,
  `img_height` int(10) DEFAULT NULL #Adding 3 new columns for avatar
);

--
-- Table structure for table `news`
--

CREATE TABLE IF NOT EXISTS `news` (
  `id` int(10) PRIMARY KEY AUTO_INCREMENT,
  `title` varchar(50),
  `text` text,
  `img_url` varchar(100) DEFAULT NULL,
  `img_width` int(10) DEFAULT NULL,
  `img_height` int(10) DEFAULT NULL,
  `date` DATETIME,
  `type` ENUM('news', 'email')
);


--
-- Table structure for table `potin`
--

CREATE TABLE IF NOT EXISTS `potin` (
  `id` int(10) PRIMARY KEY AUTO_INCREMENT,
  `title` varchar(50),
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
-- Table structure for table `groups`
--

CREATE TABLE IF NOT EXISTS `groups` (
  `id` int(10) PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(40) NOT NULL,
  `owner` varchar(40) NOT NULL,
  `beer_call` DATETIME DEFAULT NULL,
  INDEX owner_index (owner),
  FOREIGN KEY (owner)
    REFERENCES users_app(login)
    ON DELETE CASCADE
);

--
-- Table structure for table `usergroup`
--

CREATE TABLE IF NOT EXISTS `usergroup` (
  `login_user` varchar(40) NOT NULL,
  `id_group` int(10) NOT NULL,
  `status` ENUM('V', 'P') DEFAULT 'P',
  `share_position` boolean DEFAULT FALSE,
  `expiration_date` date DEFAULT NULL,
  INDEX group_index (id_group),
  FOREIGN KEY (id_group)
    REFERENCES `groups`(id)
    ON DELETE CASCADE,
  FOREIGN KEY (login_user)
    REFERENCES `users_app`(login)
    ON DELETE CASCADE,
  PRIMARY KEY(login_user, id_group)
);

--
-- Table structure for table `piste_anim`
--

CREATE TABLE IF NOT EXISTS `piste_anim` (
  `login_user` varchar(40) NOT NULL,
  `level` int(10) NOT NULL DEFAULT 0,
  INDEX group_index (login_user),
  FOREIGN KEY (login_user)
    REFERENCES `users_app`(login)
    ON DELETE CASCADE
);

--
-- Table structure for table `anim_key`
--

CREATE TABLE IF NOT EXISTS `anim_key` (
  `key` varchar(40) NOT NULL,
  `level` int(10) NOT NULL,
  `next_indice` text
);
