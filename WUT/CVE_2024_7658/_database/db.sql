-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: db
-- Generation Time: May 14, 2025 at 10:23 AM
-- Server version: 8.4.0
-- PHP Version: 8.2.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db`
--

-- --------------------------------------------------------

--
-- Table structure for table `tbl_actions_log`
--

CREATE TABLE `tbl_actions_log` (
  `id` int NOT NULL,
  `action` int NOT NULL,
  `owner_id` int NOT NULL,
  `owner_user` text,
  `affected_file` int DEFAULT NULL,
  `affected_account` int DEFAULT NULL,
  `affected_file_name` text,
  `affected_account_name` text,
  `details` text,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `tbl_actions_log`
--

INSERT INTO `tbl_actions_log` (`id`, `action`, `owner_id`, `owner_user`, `affected_file`, `affected_account`, `affected_file_name`, `affected_account_name`, `details`, `timestamp`) VALUES
(1, 0, 1, 'admin', NULL, NULL, NULL, NULL, NULL, '2025-05-14 10:08:13'),
(2, 49, 1, NULL, NULL, NULL, NULL, NULL, '{\"database_version\":\"2022102601\"}', '2025-05-14 10:08:13'),
(3, 1, 1, 'admin', NULL, NULL, NULL, 'adminfuzz', NULL, '2025-05-14 10:08:22'),
(4, 5, 1, 'admin', 1, NULL, 'invoice-12-05-2025.pdf', 'admin', NULL, '2025-05-14 10:10:21'),
(5, 32, 1, 'admin', 1, NULL, 'invoice-12-05-2025.pdf', NULL, NULL, '2025-05-14 10:10:29'),
(6, 41, 1, 'admin', 1, 1, 'invoice-12-05-2025.pdf', NULL, NULL, '2025-05-14 10:10:37'),
(7, 41, 1, 'admin', 1, 1, 'invoice-12-05-2025.pdf', NULL, NULL, '2025-05-14 10:10:48'),
(8, 41, 1, 'admin', 1, 1, 'invoice-12-05-2025.pdf', NULL, NULL, '2025-05-14 10:11:14'),
(9, 41, 0, NULL, 1, NULL, 'invoice-12-05-2025.pdf', NULL, NULL, '2025-05-14 10:15:25'),
(10, 41, 0, NULL, 1, NULL, 'invoice-12-05-2025.pdf', NULL, NULL, '2025-05-14 10:15:53'),
(11, 5, 1, 'admin', 3, NULL, 'INSTALL.txt', 'admin', NULL, '2025-05-14 10:17:12'),
(12, 32, 1, 'admin', 3, NULL, 'INSTALL.txt', NULL, NULL, '2025-05-14 10:17:17'),
(13, 5, 1, 'admin', 2, NULL, 'Screenshot from 2024-11-19 15-37-15.png', 'admin', NULL, '2025-05-14 10:19:04'),
(14, 32, 1, 'admin', 2, NULL, 'Screenshot from 2024-11-19 15-37-15.png', NULL, NULL, '2025-05-14 10:19:05'),
(15, 2, 1, 'admin', NULL, 2, NULL, 'manager', NULL, '2025-05-14 10:19:57'),
(16, 13, 1, 'admin', NULL, 2, NULL, 'manager', NULL, '2025-05-14 10:20:11'),
(17, 2, 1, 'admin', NULL, 3, NULL, 'uploader', NULL, '2025-05-14 10:20:49'),
(18, 3, 1, 'admin', NULL, 4, NULL, 'client', NULL, '2025-05-14 10:21:20');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_authentication_codes`
--

CREATE TABLE `tbl_authentication_codes` (
  `id` int NOT NULL,
  `user_id` int NOT NULL,
  `token` varchar(32) NOT NULL,
  `code` int NOT NULL,
  `used` int NOT NULL DEFAULT '0',
  `used_timestamp` timestamp NULL DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_categories`
--

CREATE TABLE `tbl_categories` (
  `id` int NOT NULL,
  `name` varchar(32) NOT NULL,
  `parent` int DEFAULT NULL,
  `description` text,
  `created_by` varchar(60) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_categories_relations`
--

CREATE TABLE `tbl_categories_relations` (
  `id` int NOT NULL,
  `file_id` int NOT NULL,
  `cat_id` int NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_cron_log`
--

CREATE TABLE `tbl_cron_log` (
  `id` int NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `sapi` varchar(32) NOT NULL,
  `results` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_custom_assets`
--

CREATE TABLE `tbl_custom_assets` (
  `id` int NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `title` varchar(500) NOT NULL,
  `content` text,
  `language` varchar(32) NOT NULL,
  `location` varchar(500) NOT NULL,
  `position` varchar(500) NOT NULL,
  `enabled` int NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_downloads`
--

CREATE TABLE `tbl_downloads` (
  `id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `file_id` int NOT NULL,
  `remote_ip` varchar(45) DEFAULT NULL,
  `remote_host` text,
  `anonymous` tinyint(1) DEFAULT '0',
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_files`
--

CREATE TABLE `tbl_files` (
  `id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `url` text NOT NULL,
  `original_url` text NOT NULL,
  `filename` text NOT NULL,
  `description` text,
  `uploader` varchar(60) NOT NULL,
  `expires` int NOT NULL DEFAULT '0',
  `expiry_date` timestamp NOT NULL DEFAULT '2026-01-01 00:00:00',
  `public_allow` int NOT NULL DEFAULT '0',
  `public_token` varchar(32) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `tbl_files`
--

INSERT INTO `tbl_files` (`id`, `user_id`, `url`, `original_url`, `filename`, `description`, `uploader`, `expires`, `expiry_date`, `public_allow`, `public_token`, `timestamp`) VALUES
(1, 1, '1747217421-d033e22ae348aeb5660fc2140aec35850c4da997-invoice-12-05-2025.pdf', 'invoice-12-05-2025.pdf', 'invoice-12-05-2025.pdf', '', 'admin', 0, '2025-06-13 00:00:00', 0, 'ETS8ByuVKmJIfov1FLPGt5OMgQrJNkvZ', '2025-05-14 10:10:21'),
(2, 1, '1747217944-d033e22ae348aeb5660fc2140aec35850c4da997-Screenshot-from-2024-11-19-15-37-15.png', 'Screenshot from 2024-11-19 15-37-15.png', 'Screenshot from 2024-11-19 15-37-15.png', '', 'admin', 0, '2025-06-13 00:00:00', 0, 'e3dUeRfcTAX1Vcf3l4ulqTJNBosYz7Je', '2025-05-14 10:19:04'),
(3, 1, '1747217832-d033e22ae348aeb5660fc2140aec35850c4da997-INSTALL.txt', 'INSTALL.txt', 'INSTALL.txt', '', 'admin', 0, '2025-06-13 00:00:00', 0, 'g1RXODcegjVo1M34tHKBTJWa7DGmEH8n', '2025-05-14 10:17:12');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_files_relations`
--

CREATE TABLE `tbl_files_relations` (
  `id` int NOT NULL,
  `file_id` int NOT NULL,
  `client_id` int DEFAULT NULL,
  `group_id` int DEFAULT NULL,
  `folder_id` int DEFAULT NULL,
  `hidden` int NOT NULL,
  `download_count` int NOT NULL DEFAULT '0',
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_folders`
--

CREATE TABLE `tbl_folders` (
  `id` int NOT NULL,
  `parent` int DEFAULT NULL,
  `name` varchar(32) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `client_id` int DEFAULT NULL,
  `group_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_groups`
--

CREATE TABLE `tbl_groups` (
  `id` int NOT NULL,
  `name` varchar(32) NOT NULL,
  `description` text,
  `public` tinyint(1) NOT NULL DEFAULT '0',
  `public_token` varchar(32) DEFAULT NULL,
  `created_by` varchar(32) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_logins_failed`
--

CREATE TABLE `tbl_logins_failed` (
  `id` int NOT NULL,
  `ip_address` varchar(60) NOT NULL,
  `username` varchar(60) NOT NULL,
  `attempted_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_members`
--

CREATE TABLE `tbl_members` (
  `id` int NOT NULL,
  `added_by` varchar(32) DEFAULT NULL,
  `client_id` int NOT NULL,
  `group_id` int NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_members_requests`
--

CREATE TABLE `tbl_members_requests` (
  `id` int NOT NULL,
  `requested_by` varchar(32) DEFAULT NULL,
  `client_id` int NOT NULL,
  `group_id` int NOT NULL,
  `denied` int NOT NULL DEFAULT '0',
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_notifications`
--

CREATE TABLE `tbl_notifications` (
  `id` int NOT NULL,
  `file_id` int NOT NULL,
  `client_id` int NOT NULL,
  `upload_type` int NOT NULL,
  `sent_status` int NOT NULL,
  `times_failed` int NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_options`
--

CREATE TABLE `tbl_options` (
  `id` int NOT NULL,
  `name` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `value` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `tbl_options`
--

INSERT INTO `tbl_options` (`id`, `name`, `value`) VALUES
(1, 'base_uri', 'http://localhost:8088/'),
(2, 'max_thumbnail_width', '100'),
(3, 'max_thumbnail_height', '100'),
(4, 'thumbnails_folder', '../../assets/img/custom/thumbs/'),
(5, 'thumbnail_default_quality', '90'),
(6, 'max_logo_width', '300'),
(7, 'max_logo_height', '300'),
(8, 'this_install_title', 'Fuzzer Test'),
(9, 'selected_clients_template', 'default'),
(10, 'logo_thumbnails_folder', '/assets/img/custom/thumbs'),
(11, 'timezone', 'UTC'),
(12, 'timeformat', 'd/m/Y'),
(13, 'allowed_file_types', '7z,ace,ai,avi,bin,bmp,bz2,cdr,csv,doc,docm,docx,eps,fla,flv,gif,gz,gzip,htm,html,iso,jpeg,jpg,mp3,mp4,mpg,odt,oog,ppt,pptx,pptm,pps,ppsx,pdf,png,psd,rar,rtf,tar,tif,tiff,tgz,txt,wav,xls,xlsm,xlsx,xz,zip'),
(14, 'logo_filename', ''),
(15, 'admin_email_address', 'admin@local.co'),
(16, 'clients_can_register', '0'),
(17, 'last_update', '1605'),
(18, 'database_version', '2022102601'),
(19, 'mail_system_use', 'mail'),
(20, 'mail_smtp_host', ''),
(21, 'mail_smtp_port', ''),
(22, 'mail_smtp_user', ''),
(23, 'mail_smtp_pass', ''),
(24, 'mail_from_name', 'Fuzzer Test'),
(25, 'thumbnails_use_absolute', '0'),
(26, 'mail_copy_user_upload', ''),
(27, 'mail_copy_client_upload', ''),
(28, 'mail_copy_main_user', ''),
(29, 'mail_copy_addresses', ''),
(30, 'version_last_check', '14-05-2025'),
(31, 'version_new_found', '0'),
(32, 'version_new_number', ''),
(33, 'version_new_url', ''),
(34, 'version_new_chlog', ''),
(35, 'version_new_security', ''),
(36, 'version_new_features', ''),
(37, 'version_new_important', ''),
(38, 'clients_auto_approve', '0'),
(39, 'clients_auto_group', '0'),
(40, 'clients_can_upload', '1'),
(41, 'clients_can_set_expiration_date', '0'),
(42, 'email_new_file_by_user_customize', '0'),
(43, 'email_new_file_by_client_customize', '0'),
(44, 'email_new_client_by_user_customize', '0'),
(45, 'email_new_client_by_self_customize', '0'),
(46, 'email_new_user_customize', '0'),
(47, 'email_new_file_by_user_text', ''),
(48, 'email_new_file_by_client_text', ''),
(49, 'email_new_client_by_user_text', ''),
(50, 'email_new_client_by_self_text', ''),
(51, 'email_new_user_text', ''),
(52, 'email_header_footer_customize', '0'),
(53, 'email_header_text', ''),
(54, 'email_footer_text', ''),
(55, 'email_pass_reset_customize', '0'),
(56, 'email_pass_reset_text', ''),
(57, 'expired_files_hide', '1'),
(58, 'notifications_max_tries', '2'),
(59, 'notifications_max_days', '15'),
(60, 'file_types_limit_to', 'all'),
(61, 'pass_require_upper', '0'),
(62, 'pass_require_lower', '0'),
(63, 'pass_require_number', '0'),
(64, 'pass_require_special', '0'),
(65, 'mail_smtp_auth', 'none'),
(66, 'use_browser_lang', '0'),
(67, 'clients_can_delete_own_files', '0'),
(68, 'google_client_id', ''),
(69, 'google_client_secret', ''),
(70, 'google_signin_enabled', '0'),
(71, 'recaptcha_enabled', '0'),
(72, 'recaptcha_site_key', ''),
(73, 'recaptcha_secret_key', ''),
(74, 'clients_can_select_group', 'none'),
(75, 'files_descriptions_use_ckeditor', '0'),
(76, 'enable_landing_for_all_files', '0'),
(77, 'footer_custom_enable', '0'),
(78, 'footer_custom_content', ''),
(79, 'email_new_file_by_user_subject_customize', '0'),
(80, 'email_new_file_by_client_subject_customize', '0'),
(81, 'email_new_client_by_user_subject_customize', '0'),
(82, 'email_new_client_by_self_subject_customize', '0'),
(83, 'email_new_user_subject_customize', '0'),
(84, 'email_pass_reset_subject_customize', '0'),
(85, 'email_new_file_by_user_subject', ''),
(86, 'email_new_file_by_client_subject', ''),
(87, 'email_new_client_by_user_subject', ''),
(88, 'email_new_client_by_self_subject', ''),
(89, 'email_new_user_subject', ''),
(90, 'email_pass_reset_subject', ''),
(91, 'privacy_noindex_site', '0'),
(92, 'email_account_approve_subject_customize', '0'),
(93, 'email_account_deny_subject_customize', '0'),
(94, 'email_account_approve_customize', '0'),
(95, 'email_account_deny_customize', '0'),
(96, 'email_account_approve_subject', ''),
(97, 'email_account_deny_subject', ''),
(98, 'email_account_approve_text', ''),
(99, 'email_account_deny_text', ''),
(100, 'email_client_edited_subject_customize', '0'),
(101, 'email_client_edited_customize', '0'),
(102, 'email_client_edited_subject', ''),
(103, 'email_client_edited_text', ''),
(104, 'public_listing_page_enable', '0'),
(105, 'public_listing_logged_only', '0'),
(106, 'public_listing_show_all_files', '0'),
(107, 'public_listing_use_download_link', '0'),
(108, 'svg_show_as_thumbnail', '0'),
(109, 'pagination_results_per_page', '10'),
(110, 'login_ip_whitelist', ''),
(111, 'login_ip_blacklist', ''),
(112, 'cron_enable', '0'),
(113, 'cron_key', 'fbf1ca55f2903b83451345954bdcff0f5b4662bb9a42f693'),
(114, 'cron_send_emails', '0'),
(115, 'cron_delete_expired_files', '0'),
(116, 'cron_delete_orphan_files', '0'),
(117, 'notifications_max_emails_at_once', '0'),
(118, 'cron_command_line_only', '1'),
(119, 'cron_email_summary_send', '0'),
(120, 'cron_email_summary_address_to', ''),
(121, 'notifications_send_when_saving_files', '1'),
(122, 'cron_save_log_database', '1'),
(123, 'cron_delete_orphan_files_types', 'not_allowed'),
(124, 'files_default_expire', '0'),
(125, 'files_default_expire_days_after', '30'),
(126, 'privacy_record_downloads_ip_address', 'all'),
(127, 'public_listing_enable_preview', '1'),
(128, 'authentication_require_email_code', '0'),
(129, 'email_2fa_code_subject_customize', '0'),
(130, 'email_2fa_code_subject', ''),
(131, 'email_2fa_code_customize', '0'),
(132, 'email_2fa_code_text', ''),
(133, 'public_listing_home_show_link', '0'),
(134, 'show_upgrade_success_message', 'false');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_password_reset`
--

CREATE TABLE `tbl_password_reset` (
  `id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `token` varchar(32) NOT NULL,
  `used` int DEFAULT '0',
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_users`
--

CREATE TABLE `tbl_users` (
  `id` int NOT NULL,
  `user` varchar(60) NOT NULL,
  `password` varchar(60) NOT NULL,
  `name` text NOT NULL,
  `email` varchar(60) NOT NULL,
  `level` tinyint(1) NOT NULL DEFAULT '0',
  `address` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `phone` varchar(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `notify` tinyint(1) NOT NULL DEFAULT '0',
  `contact` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci,
  `created_by` varchar(60) DEFAULT NULL,
  `active` tinyint(1) NOT NULL DEFAULT '1',
  `account_requested` tinyint(1) NOT NULL DEFAULT '0',
  `account_denied` tinyint(1) NOT NULL DEFAULT '0',
  `max_file_size` int NOT NULL DEFAULT '0',
  `can_upload_public` int NOT NULL DEFAULT '0',
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `tbl_users`
--

INSERT INTO `tbl_users` (`id`, `user`, `password`, `name`, `email`, `level`, `address`, `phone`, `notify`, `contact`, `created_by`, `active`, `account_requested`, `account_denied`, `max_file_size`, `can_upload_public`, `timestamp`) VALUES
(1, 'admin', '$2y$08$9AZp.oSxwBzELYcWTmHyXOrSzZm.vBh.PsiOTV57PVE/2SNJkp0DO', 'adminfuzz', 'admin@local.co', 9, NULL, NULL, 0, NULL, NULL, 1, 0, 0, 0, 0, '2025-05-14 10:08:12'),
(2, 'manager', '$2y$08$ElvRmfUJPZcNII1KIAiltuOoneWY9Wes33rp6wfnzfbFcBWugdtK2', 'manager', 'manager@local.co', 8, NULL, NULL, 0, NULL, 'admin', 1, 0, 0, 0, 0, '2025-05-14 10:19:57'),
(3, 'uploader', '$2y$08$iEkeQwHmmrYfH5338rs4O.xMZTpwV16GdytxncPu9nWjE6GfKCzwe', 'uploader', 'uploader@local.co', 7, NULL, NULL, 0, NULL, 'admin', 1, 0, 0, 0, 0, '2025-05-14 10:20:49'),
(4, 'client', '$2y$08$dWSIxQQCytwq54wcHICcd.pqL2PFRbM5D4zaPZPzG3pCVSt26V6LC', 'client', 'client@local.co', 0, NULL, NULL, 0, NULL, 'admin', 1, 0, 0, 0, 0, '2025-05-14 10:21:20');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_user_limit_upload_to`
--

CREATE TABLE `tbl_user_limit_upload_to` (
  `id` int NOT NULL,
  `user_id` int NOT NULL,
  `client_id` int NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_user_meta`
--

CREATE TABLE `tbl_user_meta` (
  `id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `value` text,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tbl_actions_log`
--
ALTER TABLE `tbl_actions_log`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tbl_authentication_codes`
--
ALTER TABLE `tbl_authentication_codes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `tbl_categories`
--
ALTER TABLE `tbl_categories`
  ADD PRIMARY KEY (`id`),
  ADD KEY `parent` (`parent`);

--
-- Indexes for table `tbl_categories_relations`
--
ALTER TABLE `tbl_categories_relations`
  ADD PRIMARY KEY (`id`),
  ADD KEY `file_id` (`file_id`),
  ADD KEY `cat_id` (`cat_id`);

--
-- Indexes for table `tbl_cron_log`
--
ALTER TABLE `tbl_cron_log`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tbl_custom_assets`
--
ALTER TABLE `tbl_custom_assets`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tbl_downloads`
--
ALTER TABLE `tbl_downloads`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `file_id` (`file_id`);

--
-- Indexes for table `tbl_files`
--
ALTER TABLE `tbl_files`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `tbl_files_relations`
--
ALTER TABLE `tbl_files_relations`
  ADD PRIMARY KEY (`id`),
  ADD KEY `file_id` (`file_id`),
  ADD KEY `client_id` (`client_id`),
  ADD KEY `group_id` (`group_id`),
  ADD KEY `folder_id` (`folder_id`);

--
-- Indexes for table `tbl_folders`
--
ALTER TABLE `tbl_folders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `parent` (`parent`),
  ADD KEY `client_id` (`client_id`),
  ADD KEY `group_id` (`group_id`);

--
-- Indexes for table `tbl_groups`
--
ALTER TABLE `tbl_groups`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tbl_logins_failed`
--
ALTER TABLE `tbl_logins_failed`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tbl_members`
--
ALTER TABLE `tbl_members`
  ADD PRIMARY KEY (`id`),
  ADD KEY `client_id` (`client_id`),
  ADD KEY `group_id` (`group_id`);

--
-- Indexes for table `tbl_members_requests`
--
ALTER TABLE `tbl_members_requests`
  ADD PRIMARY KEY (`id`),
  ADD KEY `client_id` (`client_id`),
  ADD KEY `group_id` (`group_id`);

--
-- Indexes for table `tbl_notifications`
--
ALTER TABLE `tbl_notifications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `file_id` (`file_id`),
  ADD KEY `client_id` (`client_id`);

--
-- Indexes for table `tbl_options`
--
ALTER TABLE `tbl_options`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tbl_password_reset`
--
ALTER TABLE `tbl_password_reset`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `tbl_users`
--
ALTER TABLE `tbl_users`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tbl_user_limit_upload_to`
--
ALTER TABLE `tbl_user_limit_upload_to`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `client_id` (`client_id`);

--
-- Indexes for table `tbl_user_meta`
--
ALTER TABLE `tbl_user_meta`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tbl_actions_log`
--
ALTER TABLE `tbl_actions_log`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `tbl_authentication_codes`
--
ALTER TABLE `tbl_authentication_codes`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_categories`
--
ALTER TABLE `tbl_categories`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_categories_relations`
--
ALTER TABLE `tbl_categories_relations`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_cron_log`
--
ALTER TABLE `tbl_cron_log`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_custom_assets`
--
ALTER TABLE `tbl_custom_assets`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_downloads`
--
ALTER TABLE `tbl_downloads`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_files`
--
ALTER TABLE `tbl_files`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `tbl_files_relations`
--
ALTER TABLE `tbl_files_relations`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_folders`
--
ALTER TABLE `tbl_folders`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_groups`
--
ALTER TABLE `tbl_groups`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_logins_failed`
--
ALTER TABLE `tbl_logins_failed`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_members`
--
ALTER TABLE `tbl_members`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_members_requests`
--
ALTER TABLE `tbl_members_requests`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_notifications`
--
ALTER TABLE `tbl_notifications`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_options`
--
ALTER TABLE `tbl_options`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=135;

--
-- AUTO_INCREMENT for table `tbl_password_reset`
--
ALTER TABLE `tbl_password_reset`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_users`
--
ALTER TABLE `tbl_users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `tbl_user_limit_upload_to`
--
ALTER TABLE `tbl_user_limit_upload_to`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_user_meta`
--
ALTER TABLE `tbl_user_meta`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `tbl_authentication_codes`
--
ALTER TABLE `tbl_authentication_codes`
  ADD CONSTRAINT `tbl_authentication_codes_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `tbl_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `tbl_categories`
--
ALTER TABLE `tbl_categories`
  ADD CONSTRAINT `tbl_categories_ibfk_1` FOREIGN KEY (`parent`) REFERENCES `tbl_categories` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `tbl_categories_relations`
--
ALTER TABLE `tbl_categories_relations`
  ADD CONSTRAINT `tbl_categories_relations_ibfk_1` FOREIGN KEY (`file_id`) REFERENCES `tbl_files` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `tbl_categories_relations_ibfk_2` FOREIGN KEY (`cat_id`) REFERENCES `tbl_categories` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `tbl_downloads`
--
ALTER TABLE `tbl_downloads`
  ADD CONSTRAINT `tbl_downloads_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `tbl_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `tbl_downloads_ibfk_2` FOREIGN KEY (`file_id`) REFERENCES `tbl_files` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `tbl_files`
--
ALTER TABLE `tbl_files`
  ADD CONSTRAINT `tbl_files_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `tbl_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `tbl_files_relations`
--
ALTER TABLE `tbl_files_relations`
  ADD CONSTRAINT `tbl_files_relations_ibfk_1` FOREIGN KEY (`file_id`) REFERENCES `tbl_files` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `tbl_files_relations_ibfk_2` FOREIGN KEY (`client_id`) REFERENCES `tbl_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `tbl_files_relations_ibfk_3` FOREIGN KEY (`group_id`) REFERENCES `tbl_groups` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `tbl_files_relations_ibfk_4` FOREIGN KEY (`folder_id`) REFERENCES `tbl_folders` (`id`) ON UPDATE CASCADE;

--
-- Constraints for table `tbl_folders`
--
ALTER TABLE `tbl_folders`
  ADD CONSTRAINT `tbl_folders_ibfk_1` FOREIGN KEY (`parent`) REFERENCES `tbl_folders` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `tbl_folders_ibfk_2` FOREIGN KEY (`client_id`) REFERENCES `tbl_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `tbl_folders_ibfk_3` FOREIGN KEY (`group_id`) REFERENCES `tbl_groups` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `tbl_members`
--
ALTER TABLE `tbl_members`
  ADD CONSTRAINT `tbl_members_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `tbl_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `tbl_members_ibfk_2` FOREIGN KEY (`group_id`) REFERENCES `tbl_groups` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `tbl_members_requests`
--
ALTER TABLE `tbl_members_requests`
  ADD CONSTRAINT `tbl_members_requests_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `tbl_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `tbl_members_requests_ibfk_2` FOREIGN KEY (`group_id`) REFERENCES `tbl_groups` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `tbl_notifications`
--
ALTER TABLE `tbl_notifications`
  ADD CONSTRAINT `tbl_notifications_ibfk_1` FOREIGN KEY (`file_id`) REFERENCES `tbl_files` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `tbl_notifications_ibfk_2` FOREIGN KEY (`client_id`) REFERENCES `tbl_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `tbl_password_reset`
--
ALTER TABLE `tbl_password_reset`
  ADD CONSTRAINT `tbl_password_reset_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `tbl_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `tbl_user_limit_upload_to`
--
ALTER TABLE `tbl_user_limit_upload_to`
  ADD CONSTRAINT `tbl_user_limit_upload_to_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `tbl_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `tbl_user_limit_upload_to_ibfk_2` FOREIGN KEY (`client_id`) REFERENCES `tbl_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `tbl_user_meta`
--
ALTER TABLE `tbl_user_meta`
  ADD CONSTRAINT `tbl_user_meta_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `tbl_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
