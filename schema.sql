CREATE  TABLE `sharpefolio`.`prices` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `stock_id` INT NOT NULL ,
  `date` DATE NOT NULL ,
  `closing_price` DOUBLE(10,4) UNSIGNED NOT NULL ,
  `change` DOUBLE(14,8) NOT NULL DEFAULT 0 ,
  PRIMARY KEY (`id`, `stock_id`, `date`) );
