-- phpMyAdmin SQL Dump
-- version 4.2.7.1
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: 05 Nov 2023 pada 06.13
-- Versi Server: 5.6.20
-- PHP Version: 7.4.20

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `inventaris`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `table_barang`
--

CREATE TABLE IF NOT EXISTS `table_barang` (
  `id_barang` varchar(50) NOT NULL,
  `nama_barang` varchar(50) NOT NULL,
  `kategori` varchar(50) NOT NULL,
  `merk` varchar(50) NOT NULL,
  `satuan` varchar(50) NOT NULL,
  `supplier` varchar(50) NOT NULL,
  `masa_berlaku` varchar(50) NOT NULL,
  `status` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Struktur dari tabel `table_inventaris`
--

CREATE TABLE IF NOT EXISTS `table_inventaris` (
  `id_inventaris` varchar(30) NOT NULL,
  `id_barang` varchar(30) NOT NULL,
  `tgl_maintance` date NOT NULL,
  `tgl_maintance_lanjut` date NOT NULL,
  `status` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Struktur dari tabel `table_kategori`
--

CREATE TABLE IF NOT EXISTS `table_kategori` (
  `id_kategori` varchar(30) NOT NULL,
  `nama_kategori` varchar(30) NOT NULL,
  `detail_kategori` varchar(30) NOT NULL,
  `jenis_kategori` varchar(30) NOT NULL,
  `status` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Struktur dari tabel `table_merk`
--

CREATE TABLE IF NOT EXISTS `table_merk` (
  `id_merk` varchar(30) NOT NULL,
  `nama_merk` varchar(30) NOT NULL,
  `detail_merk` varchar(30) NOT NULL,
  `status` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Struktur dari tabel `table_satuan`
--

CREATE TABLE IF NOT EXISTS `table_satuan` (
  `id_satuan` varchar(30) NOT NULL,
  `nama_satuan` varchar(30) NOT NULL,
  `detail_satuan` varchar(30) NOT NULL,
  `status` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Struktur dari tabel `table_supplier`
--

CREATE TABLE IF NOT EXISTS `table_supplier` (
  `id_supplier` varchar(50) NOT NULL,
  `nama_supplier` varchar(50) NOT NULL,
  `alamat_suplier` varchar(50) NOT NULL,
  `detail_suplier` varchar(50) NOT NULL,
  `status` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Struktur dari tabel `table_user`
--

CREATE TABLE IF NOT EXISTS `table_user` (
  `id_user` varchar(25) NOT NULL,
  `user_login` varchar(25) NOT NULL,
  `password` varchar(25) NOT NULL,
  `nama_user` varchar(25) NOT NULL,
  `nip` varchar(25) NOT NULL,
  `status` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `table_barang`
--
ALTER TABLE `table_barang`
 ADD PRIMARY KEY (`id_barang`), ADD KEY `merk` (`merk`), ADD KEY `kategori` (`kategori`), ADD KEY `supplier` (`supplier`), ADD KEY `satuan` (`satuan`);

--
-- Indexes for table `table_inventaris`
--
ALTER TABLE `table_inventaris`
 ADD PRIMARY KEY (`id_inventaris`), ADD KEY `id_barang` (`id_barang`);

--
-- Indexes for table `table_kategori`
--
ALTER TABLE `table_kategori`
 ADD PRIMARY KEY (`id_kategori`);

--
-- Indexes for table `table_merk`
--
ALTER TABLE `table_merk`
 ADD PRIMARY KEY (`id_merk`);

--
-- Indexes for table `table_satuan`
--
ALTER TABLE `table_satuan`
 ADD PRIMARY KEY (`id_satuan`);

--
-- Indexes for table `table_supplier`
--
ALTER TABLE `table_supplier`
 ADD PRIMARY KEY (`id_supplier`);

--
-- Indexes for table `table_user`
--
ALTER TABLE `table_user`
 ADD PRIMARY KEY (`id_user`);

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `table_barang`
--
ALTER TABLE `table_barang`
ADD CONSTRAINT `table_barang_ibfk_1` FOREIGN KEY (`kategori`) REFERENCES `table_kategori` (`id_kategori`),
ADD CONSTRAINT `table_barang_ibfk_2` FOREIGN KEY (`merk`) REFERENCES `table_merk` (`id_merk`),
ADD CONSTRAINT `table_barang_ibfk_3` FOREIGN KEY (`satuan`) REFERENCES `table_satuan` (`id_satuan`),
ADD CONSTRAINT `table_barang_ibfk_4` FOREIGN KEY (`supplier`) REFERENCES `table_supplier` (`id_supplier`);

--
-- Ketidakleluasaan untuk tabel `table_inventaris`
--
ALTER TABLE `table_inventaris`
ADD CONSTRAINT `table_inventaris_ibfk_1` FOREIGN KEY (`id_barang`) REFERENCES `table_barang` (`id_barang`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
