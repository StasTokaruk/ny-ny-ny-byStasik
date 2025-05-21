# SQL-скрипти

```mysql
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

DROP SCHEMA IF EXISTS `expert_survey` ;
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

DROP TABLE IF EXISTS `UserRole`, `Quiz`, `UserExpertise`, `SurveySession`, `Answer`, `SelectedOption`, `Option`, `Question`, `User`, `Role`, `ExpertiseCategory`;

CREATE TABLE `Role` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL,
  `description` VARCHAR(100) NULL,
  PRIMARY KEY (`id`)
) ENGINE = InnoDB;

CREATE TABLE `User` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `picture` MEDIUMBLOB NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `email` VARCHAR(100) NOT NULL,
  `password` VARCHAR(100) NOT NULL,
  `name` VARCHAR(50) NOT NULL,
  `surname` VARCHAR(50) NOT NULL,
  `nickname` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE = InnoDB;

CREATE TABLE `UserRole` (
  `User_id` INT NOT NULL,
  `Role_id` INT NOT NULL,
  INDEX `fk_UserRole_Role_idx` (`Role_id` ASC),
  INDEX `fk_UserRole_User1_idx` (`User_id` ASC),
  CONSTRAINT `fk_UserRole_Role`
    FOREIGN KEY (`Role_id`) REFERENCES `Role` (`id`)
    ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_UserRole_User1`
    FOREIGN KEY (`User_id`) REFERENCES `User` (`id`)
    ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;

CREATE TABLE `Quiz` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `created_by` INT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `name` VARCHAR(100) NULL,
  `description` VARCHAR(255) NULL,
  `User_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_Quiz_User1_idx` (`User_id` ASC),
  CONSTRAINT `fk_Quiz_User1`
    FOREIGN KEY (`User_id`) REFERENCES `User` (`id`)
    ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;

CREATE TABLE `ExpertiseCategory` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50) NULL,
  `description` VARCHAR(100) NULL,
  PRIMARY KEY (`id`)
) ENGINE = InnoDB;

CREATE TABLE `UserExpertise` (
  `ExpertiseCategory_id` INT NOT NULL,
  `User_id` INT NOT NULL,
  INDEX `fk_UserExpertise_ExpertiseCategory1_idx` (`ExpertiseCategory_id` ASC),
  INDEX `fk_UserExpertise_User1_idx` (`User_id` ASC),
  CONSTRAINT `fk_UserExpertise_ExpertiseCategory1`
    FOREIGN KEY (`ExpertiseCategory_id`) REFERENCES `ExpertiseCategory` (`id`)
    ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_UserExpertise_User1`
    FOREIGN KEY (`User_id`) REFERENCES `User` (`id`)
    ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;

CREATE TABLE `Question` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `Quiz_id` INT NOT NULL,
  `number` INT NULL,
  `description` VARCHAR(255) NULL,
  `type` VARCHAR(45) NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_Question_Quiz1_idx` (`Quiz_id` ASC),
  CONSTRAINT `fk_Question_Quiz1`
    FOREIGN KEY (`Quiz_id`) REFERENCES `Quiz` (`id`)
    ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;

CREATE TABLE `SurveySession` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `User_id` INT NOT NULL,
  `Quiz_id` INT NOT NULL,
  `started_at` DATETIME NULL,
  `completed_at` DATETIME NULL,
  `status` VARCHAR(45) NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_SurveySession_User1_idx` (`User_id` ASC),
  INDEX `fk_SurveySession_Quiz1_idx` (`Quiz_id` ASC),
  CONSTRAINT `fk_SurveySession_User1`
    FOREIGN KEY (`User_id`) REFERENCES `User` (`id`)
    ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_SurveySession_Quiz1`
    FOREIGN KEY (`Quiz_id`) REFERENCES `Quiz` (`id`)
    ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;

CREATE TABLE `Option` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `Question_id` INT NOT NULL,
  `number` INT NULL,
  `description` INT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_Option_Question1_idx` (`Question_id` ASC),
  CONSTRAINT `fk_Option_Question1`
    FOREIGN KEY (`Question_id`) REFERENCES `Question` (`id`)
    ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;

CREATE TABLE `Answer` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `SurveySession_id` INT NOT NULL,
  `Question_id` INT NOT NULL,
  `file` MEDIUMBLOB NULL,
  `text` VARCHAR(255) NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_Answer_Question1_idx` (`Question_id` ASC),
  INDEX `fk_Answer_SurveySession1_idx` (`SurveySession_id` ASC),
  CONSTRAINT `fk_Answer_Question1`
    FOREIGN KEY (`Question_id`) REFERENCES `Question` (`id`)
    ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_Answer_SurveySession1`
    FOREIGN KEY (`SurveySession_id`) REFERENCES `SurveySession` (`id`)
    ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;

CREATE TABLE `SelectedOption` (
  `Answer_id` INT NOT NULL,
  `Option_id` INT NOT NULL,
  INDEX `fk_SelectedOption_Option1_idx` (`Option_id` ASC),
  INDEX `fk_SelectedOption_Answer1_idx` (`Answer_id` ASC),
  CONSTRAINT `fk_SelectedOption_Option1`
    FOREIGN KEY (`Option_id`) REFERENCES `Option` (`id`)
    ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_SelectedOption_Answer1`
    FOREIGN KEY (`Answer_id`) REFERENCES `Answer` (`id`)
    ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
```
