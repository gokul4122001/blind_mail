-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Feb 27, 2023 at 07:11 PM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `blind_mail`
--

-- --------------------------------------------------------

--
-- Table structure for table `contact`
--

CREATE TABLE `contact` (
  `id` int(11) NOT NULL,
  `uname` varchar(30) NOT NULL,
  `cname` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `contact`
--


-- --------------------------------------------------------

--
-- Table structure for table `receiver`
--

CREATE TABLE `receiver` (
  `id` int(11) NOT NULL,
  `fid` int(11) NOT NULL,
  `uname` varchar(30) NOT NULL,
  `send_to` varchar(100) NOT NULL,
  `subject` varchar(100) NOT NULL,
  `message` text NOT NULL,
  `pimage` varchar(50) NOT NULL,
  `rdate` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  `view_st` int(11) NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `receiver`
--

INSERT INTO `receiver` (`id`, `fid`, `uname`, `send_to`, `subject`, `message`, `pimage`, `rdate`, `view_st`, `status`) VALUES
(1, 0, 'raja123@gmail.com', 'sam@gmail.com', 'hi', 'very very good morning wonderful day today is saturday', '7.jpg', '2023-02-28 00:41:00', 1, 1),
(2, 0, 'raja123@gmail.com', 'sam@gmail.com', 'hello', 'today is very beautiful very rainy day today is saturday', '3.jpg', '2023-02-28 00:27:40', 1, 1),
(3, 0, 'raja123@gmail.com', 'sam@gmail.com', 'hello.', 'how are you?', '', '2023-02-28 00:23:39', 1, 0),
(6, 0, 'sam@gmail.com', 'raja123@gmail.com', 'good', 'very nice design', '', '2023-02-28 00:35:04', 1, 0);

-- --------------------------------------------------------

--
-- Table structure for table `register`
--

CREATE TABLE `register` (
  `id` int(11) NOT NULL,
  `name` varchar(30) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `contact` bigint(20) NOT NULL,
  `city` varchar(30) NOT NULL,
  `username` varchar(30) NOT NULL,
  `password` varchar(30) NOT NULL,
  `rdate` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `register`
--

INSERT INTO `register` (`id`, `name`, `gender`, `contact`, `city`, `username`, `password`, `rdate`) VALUES
(1, 'Raja', 'Male.', 0, 'Trichy.', 'raja123@gmail.com', '123.', '27-02-2023'),
(2, 'thank you for coming over.', 'hi baby, i', 0, 'really.', 'really.', 'are they going to be able?', '27-02-2023'),
(3, 'sam.', 'male', 0, 'salem', 'sam@gmail.com', '123.', '28-02-2023');

-- --------------------------------------------------------

--
-- Table structure for table `sender`
--

CREATE TABLE `sender` (
  `id` int(11) NOT NULL,
  `uname` varchar(30) NOT NULL,
  `send_to` varchar(50) NOT NULL,
  `subject` varchar(100) NOT NULL,
  `message` text NOT NULL,
  `filename` varchar(50) NOT NULL,
  `rdate` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `sender`
--


-- --------------------------------------------------------

--
-- Table structure for table `user_files`
--

CREATE TABLE `user_files` (
  `id` int(11) NOT NULL,
  `mid` int(11) NOT NULL,
  `uname` varchar(30) NOT NULL,
  `fname` varchar(50) NOT NULL,
  `ftype` varchar(100) NOT NULL,
  `fsize` double NOT NULL,
  `file_st` int(11) NOT NULL,
  `dtime` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user_files`
--

