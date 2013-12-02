CREATE  TABLE `sharpefolio`.`prices` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `stock_id` INT NOT NULL ,
  `date` DATE NOT NULL ,
  `closing_price` DOUBLE(10,4) UNSIGNED NOT NULL ,
  `change` DOUBLE(14,8) NOT NULL DEFAULT 0 ,
  PRIMARY KEY (`id`, `stock_id`, `date`)
) ENGINE=InnoDB AUTO_INCREMENT=7935 DEFAULT CHARSET=utf8;

CREATE TABLE `stocks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `symbol` varchar(50) NOT NULL,
  `company` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`,`symbol`)
) ENGINE=InnoDB AUTO_INCREMENT=7935 DEFAULT CHARSET=utf8;
