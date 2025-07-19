-- phpMyAdmin SQL Dump
-- version 5.1.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 30, 2023 at 04:41 AM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.1.5

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Database: `oews_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `cart_list`
--

CREATE TABLE `cart_list` (
  `id` int(30) NOT NULL,
  `customer_id` int(30) NOT NULL,
  `product_id` int(30) NOT NULL,
  `quantity` int(30) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `cart_list`
--

INSERT INTO `cart_list` (`id`, `customer_id`, `product_id`, `quantity`) VALUES
(4, 1, 1, 1),
(5, 1, 5, 1);

-- --------------------------------------------------------

--
-- Table structure for table `category_list`
--

CREATE TABLE `category_list` (
  `id` int(30) NOT NULL,
  `name` text NOT NULL,
  `description` text NOT NULL,
  `status` tinyint(1) NOT NULL DEFAULT 1,
  `delete_flag` tinyint(1) NOT NULL DEFAULT 0,
  `date_created` datetime NOT NULL DEFAULT current_timestamp(),
  `date_updated` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `category_list`
--

INSERT INTO `category_list` (`id`, `name`, `description`, `status`, `delete_flag`, `date_created`, `date_updated`) VALUES
(1, 'Sports Eye Protection', 'Sports eyewear is an ideal option for various activities whether indoor or outdoor. Lenses with impact resistance are important types of eyewear to help prevent any injuries to the eyes and keeping dust away. An anti-glare coating can help with glare from indoor lighting in a gymnasium or stadium-lit settings.', 1, 0, '2023-01-30 10:03:37', '2023-01-30 10:03:37'),
(2, 'Sunglasses', 'Prescription sunglasses are one of the most important types of eyewear with many modifications.  Sunglasses that have lenses with your eyes specific prescription designed into them, can help you see clearly while reducing the brightness and glare from your surroundings.', 1, 0, '2023-01-30 10:05:04', '2023-01-30 10:05:04'),
(3, 'Safety Glasses', 'Real Eyes Optometry carries a wide variety of Canadian safety approved types of eyewear and safety standard lenses. We will work with you to determine the most appropriate safety eyewear for your particular occupation.', 1, 0, '2023-01-30 10:06:13', '2023-01-30 10:06:13');

-- --------------------------------------------------------

--
-- Table structure for table `customer_list`
--

CREATE TABLE `customer_list` (
  `id` int(30) NOT NULL,
  `firstname` text NOT NULL,
  `middlename` text DEFAULT NULL,
  `lastname` text NOT NULL,
  `gender` varchar(100) NOT NULL,
  `contact` text NOT NULL,
  `email` text NOT NULL,
  `password` text NOT NULL,
  `avatar` text DEFAULT NULL,
  `date_created` datetime NOT NULL DEFAULT current_timestamp(),
  `date_updated` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `customer_list`
--

INSERT INTO `customer_list` (`id`, `firstname`, `middlename`, `lastname`, `gender`, `contact`, `email`, `password`, `avatar`, `date_created`, `date_updated`) VALUES
(1, 'Mark', 'D', 'Cooper', 'Male', '0912356498', 'mcooper@mail.com', 'c7162ff89c647f444fcaa5c635dac8c3', 'uploads/customers/1.png?v=1675045908', '2023-01-30 10:31:48', '2023-01-30 10:49:25');

-- --------------------------------------------------------

--
-- Table structure for table `order_items`
--

CREATE TABLE `order_items` (
  `order_id` int(30) NOT NULL,
  `product_id` int(30) NOT NULL,
  `quantity` int(30) NOT NULL DEFAULT 0,
  `price` float(12,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `order_items`
--

INSERT INTO `order_items` (`order_id`, `product_id`, `quantity`, `price`) VALUES
(2, 1, 2, 355.99),
(2, 2, 2, 455.99);

-- --------------------------------------------------------

--
-- Table structure for table `order_list`
--

CREATE TABLE `order_list` (
  `id` int(30) NOT NULL,
  `code` varchar(100) NOT NULL,
  `customer_id` int(30) NOT NULL,
  `delivery_address` text NOT NULL,
  `total_amount` float(12,2) NOT NULL DEFAULT 0.00,
  `status` tinyint(1) NOT NULL DEFAULT 0 COMMENT '0=pending,\r\n1=packed,\r\n2=out for delivery,\r\n3=paid\r\n',
  `date_created` datetime NOT NULL DEFAULT current_timestamp(),
  `date_updated` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `order_list`
--

INSERT INTO `order_list` (`id`, `code`, `customer_id`, `delivery_address`, `total_amount`, `status`, `date_created`, `date_updated`) VALUES
(2, '2023013000002', 1, 'Sample Address only 101', 1623.96, 3, '2023-01-30 10:34:56', '2023-01-30 10:51:56');

-- --------------------------------------------------------

--
-- Table structure for table `product_list`
--

CREATE TABLE `product_list` (
  `id` int(30) NOT NULL,
  `category_id` int(30) NOT NULL,
  `brand` text NOT NULL,
  `name` text NOT NULL,
  `description` text NOT NULL,
  `dose` varchar(250) NOT NULL,
  `price` float(12,2) NOT NULL DEFAULT 0.00,
  `image_path` text DEFAULT NULL,
  `status` tinyint(1) NOT NULL DEFAULT 1,
  `delete_flag` tinyint(1) NOT NULL DEFAULT 0,
  `date_created` datetime NOT NULL DEFAULT current_timestamp(),
  `date_updated` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `product_list`
--

INSERT INTO `product_list` (`id`, `category_id`, `brand`, `name`, `description`, `dose`, `price`, `image_path`, `status`, `delete_flag`, `date_created`, `date_updated`) VALUES
(1, 2, 'Brand 101', 'Sunglasses 101', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris vulputate vestibulum massa, eget ultricies nisi cursus quis.', '', 355.99, 'uploads/medicines//ew5.jpg?v=1675044474', 1, 0, '2023-01-30 10:07:54', '2023-01-30 10:07:54'),
(2, 2, 'Brand 101', 'Sunglass 102', 'Mauris fermentum vitae sem et ornare. Sed fermentum tellus non libero eleifend, et vehicula orci laoreet.', '', 455.99, 'uploads/medicines//ew4.jpg?v=1675044510', 1, 0, '2023-01-30 10:08:30', '2023-01-30 10:08:30'),
(3, 2, 'Brand 102', 'Sunglass 103', 'Donec eget purus quam. Aliquam erat volutpat. Nulla facilisi. Proin interdum ultrices faucibus. Nunc ornare lacus eget diam hendrerit, eget ullamcorper ligula egestas.', '', 788.99, 'uploads/medicines//ew2.jpg?v=1675044548', 1, 0, '2023-01-30 10:09:08', '2023-01-30 10:09:08'),
(4, 1, 'Brand 103', 'Sports Eyewear 101', 'Sed tincidunt consequat enim in porttitor. Pellentesque purus augue, hendrerit a varius id, tristique id erat. Phasellus at iaculis elit. Nunc sed turpis ac ex sagittis fringilla.', '', 1099.99, 'uploads/medicines//sport-ew-1.jpg?v=1675044738', 1, 0, '2023-01-30 10:12:18', '2023-01-30 10:12:18'),
(5, 1, 'Brand 104', 'Sports Eyewear 102', 'Nulla facilisi. Suspendisse molestie commodo blandit. Donec est dolor, viverra vel ultricies ut, accumsan eu libero. Quisque et lectus vehicula sapien vehicula dapibus ut a metus. Sed in lacus quam.', '', 2599.99, 'uploads/medicines//sport-ew-2.jpg?v=1675044773', 1, 0, '2023-01-30 10:12:53', '2023-01-30 10:12:53'),
(6, 3, 'Brand 105', 'Eye Protector 101', 'Fusce rutrum turpis in odio ornare tristique. Aenean molestie ullamcorper nibh id dictum. Integer sollicitudin dapibus suscipit. Sed eleifend sapien tortor, eget laoreet felis tempus in.', '', 399.99, 'uploads/medicines//eye-p-1.jpg?v=1675044909', 1, 0, '2023-01-30 10:15:09', '2023-01-30 10:15:09'),
(7, 3, 'Brand 105', 'Eye Protector 102', 'Duis consectetur ex nec elit fermentum, euismod scelerisque ex tincidunt. Ut eget est imperdiet, pretium sapien at, semper mi.', '', 599.99, 'uploads/medicines//eye-p-2.jpg?v=1675044956', 1, 0, '2023-01-30 10:15:56', '2023-01-30 10:15:56'),
(8, 3, 'Brand 106', 'Eye Protector 103', 'Vestibulum convallis quam sit amet turpis porta blandit. Donec dictum interdum porta. Morbi odio dui, ultricies sit amet dignissim sit amet, volutpat sed libero.', '', 699.99, 'uploads/medicines//eye-p-3.jpg?v=1675045002', 1, 0, '2023-01-30 10:16:42', '2023-01-30 10:16:42');

-- --------------------------------------------------------

--
-- Table structure for table `stock_list`
--

CREATE TABLE `stock_list` (
  `id` int(30) NOT NULL,
  `product_id` int(30) NOT NULL,
  `code` varchar(100) NOT NULL,
  `quantity` float(12,2) NOT NULL DEFAULT 0.00,
  `date_created` datetime NOT NULL DEFAULT current_timestamp(),
  `date_updated` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `stock_list`
--

INSERT INTO `stock_list` (`id`, `product_id`, `code`, `quantity`, `date_created`, `date_updated`) VALUES
(1, 2, 'Asd87A546', 50.00, '2023-01-30 10:24:29', '2023-01-30 10:24:29'),
(2, 1, 'SDA12312', 50.00, '2023-01-30 10:25:22', '2023-01-30 10:25:22'),
(3, 3, 'GH272711', 100.00, '2023-01-30 10:25:40', '2023-01-30 10:25:40'),
(4, 4, '878751A122', 150.00, '2023-01-30 10:26:03', '2023-01-30 10:26:03'),
(5, 5, 'FAD78885', 40.00, '2023-01-30 10:26:22', '2023-01-30 10:26:22'),
(6, 6, '879ASC', 80.00, '2023-01-30 10:26:34', '2023-01-30 10:26:34'),
(7, 7, '879SAC878', 100.00, '2023-01-30 10:26:48', '2023-01-30 10:26:48'),
(8, 8, 'LEST123454', 75.00, '2023-01-30 10:27:04', '2023-01-30 10:27:04');

-- --------------------------------------------------------

--
-- Table structure for table `stock_out`
--

CREATE TABLE `stock_out` (
  `id` int(30) NOT NULL,
  `order_id` int(30) NOT NULL,
  `stock_id` int(30) NOT NULL,
  `quantity` int(30) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `system_info`
--

CREATE TABLE `system_info` (
  `id` int(30) NOT NULL,
  `meta_field` text NOT NULL,
  `meta_value` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `system_info`
--

INSERT INTO `system_info` (`id`, `meta_field`, `meta_value`) VALUES
(1, 'name', 'Online Eyewear Shop - PHP'),
(6, 'short_name', 'OEWS - PHP'),
(11, 'logo', 'uploads/logo.png?v=1675042833'),
(13, 'user_avatar', 'uploads/user_avatar.jpg'),
(14, 'cover', 'uploads/cover.png?v=1675042834'),
(17, 'phone', '456-987-1231'),
(18, 'mobile', '09123456987 / 094563212222 '),
(19, 'email', 'info@sample.com'),
(20, 'address', '7087 Henry St. Clifton Park, NY 12065');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(50) NOT NULL,
  `firstname` varchar(250) NOT NULL,
  `middlename` text DEFAULT NULL,
  `lastname` varchar(250) NOT NULL,
  `username` text NOT NULL,
  `password` text NOT NULL,
  `avatar` text DEFAULT NULL,
  `last_login` datetime DEFAULT NULL,
  `type` tinyint(1) NOT NULL DEFAULT 0,
  `date_added` datetime NOT NULL DEFAULT current_timestamp(),
  `date_updated` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='2';

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `firstname`, `middlename`, `lastname`, `username`, `password`, `avatar`, `last_login`, `type`, `date_added`, `date_updated`) VALUES
(1, 'Adminstrator', '', 'Admin', 'admin', '0192023a7bbd73250516f069df18b500', 'uploads/avatars/1.png?v=1649834664', NULL, 1, '2021-01-20 14:02:37', '2022-05-16 14:17:49'),
(8, 'Claire', '', 'Blake', 'cblake', 'cd74fae0a3adf459f73bbf187607ccea', 'uploads/avatars/8.png?v=1675047323', NULL, 2, '2023-01-30 10:55:23', '2023-01-30 10:55:23');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cart_list`
--
ALTER TABLE `cart_list`
  ADD PRIMARY KEY (`id`),
  ADD KEY `customer_id` (`customer_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `category_list`
--
ALTER TABLE `category_list`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `customer_list`
--
ALTER TABLE `customer_list`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `order_items`
--
ALTER TABLE `order_items`
  ADD KEY `order_id` (`order_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `order_list`
--
ALTER TABLE `order_list`
  ADD PRIMARY KEY (`id`),
  ADD KEY `customer_id` (`customer_id`);

--
-- Indexes for table `product_list`
--
ALTER TABLE `product_list`
  ADD PRIMARY KEY (`id`),
  ADD KEY `category_id` (`category_id`);

--
-- Indexes for table `stock_list`
--
ALTER TABLE `stock_list`
  ADD PRIMARY KEY (`id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `stock_out`
--
ALTER TABLE `stock_out`
  ADD PRIMARY KEY (`id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `stock_id` (`stock_id`);

--
-- Indexes for table `system_info`
--
ALTER TABLE `system_info`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `cart_list`
--
ALTER TABLE `cart_list`
  MODIFY `id` int(30) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `category_list`
--
ALTER TABLE `category_list`
  MODIFY `id` int(30) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `customer_list`
--
ALTER TABLE `customer_list`
  MODIFY `id` int(30) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `order_list`
--
ALTER TABLE `order_list`
  MODIFY `id` int(30) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `product_list`
--
ALTER TABLE `product_list`
  MODIFY `id` int(30) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `stock_list`
--
ALTER TABLE `stock_list`
  MODIFY `id` int(30) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `stock_out`
--
ALTER TABLE `stock_out`
  MODIFY `id` int(30) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `system_info`
--
ALTER TABLE `system_info`
  MODIFY `id` int(30) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `cart_list`
--
ALTER TABLE `cart_list`
  ADD CONSTRAINT `customer_id_fk_cl` FOREIGN KEY (`customer_id`) REFERENCES `customer_list` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  ADD CONSTRAINT `product_id_fk_cl` FOREIGN KEY (`product_id`) REFERENCES `product_list` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION;

--
-- Constraints for table `order_items`
--
ALTER TABLE `order_items`
  ADD CONSTRAINT `order_id_fk_oi` FOREIGN KEY (`order_id`) REFERENCES `order_list` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  ADD CONSTRAINT `product_id_fk_oi` FOREIGN KEY (`product_id`) REFERENCES `product_list` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION;

--
-- Constraints for table `order_list`
--
ALTER TABLE `order_list`
  ADD CONSTRAINT `customer_id_fk_ol` FOREIGN KEY (`customer_id`) REFERENCES `customer_list` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION;

--
-- Constraints for table `product_list`
--
ALTER TABLE `product_list`
  ADD CONSTRAINT `category_id_fk_pl` FOREIGN KEY (`category_id`) REFERENCES `category_list` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION;

--
-- Constraints for table `stock_list`
--
ALTER TABLE `stock_list`
  ADD CONSTRAINT `product_id_fk_sl` FOREIGN KEY (`product_id`) REFERENCES `product_list` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION;

--
-- Constraints for table `stock_out`
--
ALTER TABLE `stock_out`
  ADD CONSTRAINT `order_id_fk_so` FOREIGN KEY (`order_id`) REFERENCES `order_list` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  ADD CONSTRAINT `stock_id_fk_so` FOREIGN KEY (`stock_id`) REFERENCES `stock_list` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION;
COMMIT;
