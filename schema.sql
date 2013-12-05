CREATE  TABLE `sharpefolio`.`prices` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `stock_id` INT NOT NULL ,
  `date` date NOT NULL ,
  `closing_price` double(10,4) UNSIGNED NOT NULL ,
  `change` double(14,8) NOT NULL DEFAULT 0 ,
  PRIMARY KEY (`id`, `stock_id`, `date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `stocks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `symbol` varchar(50) NOT NULL,
  `company` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`,`symbol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `reports` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `duration` int(11) NOT NULL,
  `formula` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_report` (`date`, `duration`, `formula`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `ratios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stock_id` int(11) NOT NULL,
  `report_id` int(11) NOT NULL,
  `ratio` double(10,6),
  PRIMARY KEY (`id`, `stock_id`, `report_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `picks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `recipe_id` int(11) NOT NULL,
  `stock_id` int(11) NOT NULL,
  `gain` double(10,6),
  `weight` double(10,6),
  PRIMARY KEY (`id`, `recipe_id`, `stock_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `recipes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `recipe_id` int(11) NOT NULL,
  `n_stocks` int(11) NOT NULL,
  `check_correlation` tinyint(1) UNSIGNED NOT NULL,
  `distribution` double(10,6),
  PRIMARY KEY (`id`, `recipe_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

ALTER TABLE `sharpefolio`.`prices`
ADD UNIQUE INDEX `unique_price` (`stock_id` ASC, `date` ASC);
