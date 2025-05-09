CREATE DATABASE IF NOT EXISTS `proctorai` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `proctorai`;

DROP TABLE IF EXISTS `reportlog`;
DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `proctor_name` varchar(255) NOT NULL UNIQUE,
  `email` varchar(255) NOT NULL UNIQUE,
  `password` varchar(255) NOT NULL,
  `user_role` ENUM('admin', 'proctor') NOT NULL DEFAULT 'proctor',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `reportlog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `num_students` int NOT NULL,
  `block` varchar(255) NOT NULL,
  `subject` varchar(255) NOT NULL,
  `room` varchar(255) NOT NULL,
  `start` TIME NOT NULL,
  `end` TIME NOT NULL,
  `date` date NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_reportlog_user` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- sample admin user with a hashed password of 'administrator'
-- Note: The password is hashed using SHA256.
-- username: admin
-- email: admin@example.com
-- password: administrator
INSERT INTO users (proctor_name, email, password, user_role)
VALUES ('admin', 'admin@example.com', '4194d1706ed1f408d5e02d672777019f4d5385c766a8c6ca8acba3167d36a7b9', 'admin');
