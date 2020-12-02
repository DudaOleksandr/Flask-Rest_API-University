CREATE DATABASE IF NOT EXISTS `lab5` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `lab5`;

CREATE TABLE `product` (
  `id` int(11) NOT NULL,
  `name` varchar(32) DEFAULT NULL,
  `status` varchar(32) DEFAULT NULL,
  `amount` int(11) DEFAULT NULL,
  `is_bought` tinyint(1) DEFAULT NULL,
  `purchase_id` int(11) DEFAULT NULL
) ;

CREATE TABLE `product_list` (
  `id` int(11) NOT NULL,
  `name` varchar(32) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `purchase` (
  `id` int(11) NOT NULL,
  `quantity` int(11) DEFAULT NULL,
  `userID` int(11) DEFAULT NULL,
  `shipDate` varchar(64) DEFAULT NULL,
  `complete` tinyint(1) DEFAULT NULL,
  `status` varchar(32) DEFAULT NULL
) ;

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(32) DEFAULT NULL,
  `email` varchar(32) DEFAULT NULL,
  `password` varchar(32) DEFAULT NULL,
  `user_status` varchar(32) DEFAULT NULL,
  `status` varchar(32) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


ALTER TABLE `product`
  ADD PRIMARY KEY (`id`),
  ADD KEY `purchase_id` (`purchase_id`);

ALTER TABLE `product_list`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `purchase`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);


ALTER TABLE `product`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `product_list`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `purchase`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;


ALTER TABLE `product`
  ADD CONSTRAINT `product_ibfk_1` FOREIGN KEY (`purchase_id`) REFERENCES `purchase` (`id`);
COMMIT;

