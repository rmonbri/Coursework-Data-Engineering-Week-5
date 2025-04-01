--Schema for lmnh_plants database. Will create tables under 'dbo' schema (default)

USE lmnh_plants;
GO

DROP TABLE IF EXISTS measurement, plant, plant_type, botanist, origin;


CREATE TABLE plant_type (
    plant_type_id TINYINT IDENTITY(1,1) PRIMARY KEY,
    plant_name VARCHAR(50) NOT NULL,
    scientific_name VARCHAR(50)
);

CREATE TABLE botanist (
    botanist_id TINYINT IDENTITY(1,1) PRIMARY KEY,
    botanist_number VARCHAR(20) NOT NULL,
    botanist_email VARCHAR(50) NOT NULL,
    botanist_name VARCHAR(30) NOT NULL
);

CREATE TABLE origin (
    location_id TINYINT IDENTITY(1,1) PRIMARY KEY,
    latitude DECIMAL(9, 6) NOT NULL,
    longitude DECIMAL(9, 6) NOT NULL,
    locality VARCHAR(40) NOT NULL,
    country_code VARCHAR(2) NOT NULL,
    timezone VARCHAR(40) NOT NULL
);

CREATE TABLE plant (
    plant_id TINYINT IDENTITY(1,1) PRIMARY KEY,
    botanist_id TINYINT NOT NULL,
    plant_type_id TINYINT NOT NULL,
    location_id TINYINT NOT NULL,
    CONSTRAINT FK_botanist_id FOREIGN KEY (botanist_id) REFERENCES botanist (botanist_id),
    CONSTRAINT FK_plant_type_id FOREIGN KEY (plant_type_id) REFERENCES plant_type (plant_type_id),
    CONSTRAINT FK_location_id FOREIGN KEY (location_id) REFERENCES origin (location_id),
);

CREATE TABLE measurement (
    measurement_id BIGINT IDENTITY(1,1) PRIMARY KEY,
    plant_id TINYINT NOT NULL,
    measurement_time DATETIME NOT NULL,
    last_watered DATETIME NOT NULL,
    moisture FLOAT NOT NULL,
    temperature FLOAT NOT NULL,
    CONSTRAINT FK_plant_id FOREIGN KEY (plant_id) REFERENCES plant (plant_id)
);
GO