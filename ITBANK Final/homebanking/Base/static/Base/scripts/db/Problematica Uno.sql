--- 1) Crear en la base de datos los tipos de cliente, de cuenta y marcas de tarjeta. Insertar los valores según la información provista en el Sprint 5

CREATE TABLE IF NOT EXISTS tipo_cliente (
	typing_id INTEGER PRIMARY KEY,
	typing TEXT NOT NULL
);

INSERT INTO tipo_cliente (typing) VALUES 
	('BLACK'),
	('GOLD'),
	('CLASSIC');


BEGIN TRANSACTION;

CREATE TABLE cliente_actualizado (
	customer_id INTEGER PRIMARY KEY,
    customer_type_id INTEGER,
	customer_name TEXT NOT NULL,
	customer_surname NUMERIC NOT NULL,
	customer_DNI TEXT NOT NULL,
	dob TEXT,
	branch_id INTEGER NOT NULL,
	FOREIGN KEY(customer_type_id) REFERENCES tipo_cliente(typing_id)
);

INSERT INTO cliente_actualizado SELECT * FROM cliente;

DROP TABLE cliente;

ALTER TABLE cliente_actualizado RENAME TO cliente;

COMMIT;


CREATE TABLE IF NOT EXISTS tipo_cuenta (
	typing_id INTEGER PRIMARY KEY,
	typing TEXT NOT NULL
);

INSERT INTO tipo_cuenta (typing) VALUES
	('CUENTA CORRIENTE'),
	('CAJA AHORRO DOLARES'),
	('CAJA AHORRO PESOS');

CREATE TABLE IF NOT EXISTS marca_tarjeta (
	brand_id INTEGER PRIMARY KEY,
	brand TEXT NOT NULL
);

INSERT INTO marca_tarjeta (brand) VALUES
	('Visa'),
	('MasterCard'),
	('American Express'),
	('Discover'),
	('Carte Blanche');


--- 2) Agregar la entidad tarjeta teniendo en cuenta los atributos necesarios para la operación del home banking 
--- (se sugieren los siguientes campos Numero (único e irrepetible, con una restricción ante cada inserción que no debe superar 20 números/espacios), 
--- CVV, Fecha de otorgamiento, Fecha Expiración). Almacenar si es una tarjeta de crédito o débito.

--- 3) Relacionar las tarjetas con la tabla donde se guardan las marcas de tarjeta

--- 4) Relacionar las tarjetas con el cliente al que pertenecen

CREATE TABLE IF NOT EXISTS tarjeta (
	card_number NUMERIC CHECK(length(card_number) <= 20) PRIMARY KEY,
	customer_id INTEGER,
	card_brand_id INTEGER,
	card_verification_value INTEGER CHECK(length(card_verification_value) == 3),
	card_type TEXT CHECK(card_type IN ('DEBIT','CREDIT')) NOT NULL,
	creation_date TEXT GENERATED ALWAYS AS (DATE('now')) STORED,
	expiration_date TEXT GENERATED ALWAYS AS (DATE('now', '+5 years')) STORED,
	FOREIGN KEY(customer_id) REFERENCES cliente(customer_id),
	FOREIGN KEY(card_brand_id) REFERENCES marca_tarjeta(brand_id)
);

--- 5) Insertar 500 tarjetas de crédito con sus respectivos datos (www.generatedata.com) asociándolas a los clientes de forma aleatoria

--- Para este paso es necesario importar como tabla el archivo adjunto 'card_data.csv' por medio de la consola o por DB Browser, no encontre un modo
--- programatico para lograrlo. Una vez hecho esto, con ejecutar esta Query deberia bastar para establecer la tabla como se debe


BEGIN TRANSACTION;

INSERT INTO tarjeta SELECT * FROM card_data;

DROP card_data;

COMMIT;


--- 6) Agregar la entidad direcciones, que puede ser usada por los clientes, empleados y sucursales con los campos utilizados en el SPRINT 5

CREATE TABLE IF NOT EXISTS direccion (
	address_id INTEGER PRIMARY KEY,
	country TEXT NOT NULL,
	province TEXT NOT NULL,
	city TEXT NOT NULL,
	address_name TEXT NOT NULL
);

--- 7) Insertar 500 direcciones, asignando del lote inicial a empleados, clientes o sucursal de forma aleatoria.
--- Teniendo en cuenta que un cliente o empleado puede tener múltiples direcciones, pero la sucursal, solo una.

--- Del mismo modo que el punto 5, para este paso es necesario importar como tabla el archivo 'address_data.csv' por medio de la consola o por DB Browser,
--- no encontre un modo programatico para lograrlo. Una vez hecho esto, con ejecutar esta Query deberia bastar para establecer la tabla como se debe


BEGIN TRANSACTION;

INSERT INTO direccion SELECT * FROM address_data;

DROP address_data;

COMMIT;


CREATE TABLE IF NOT EXISTS direccion_cliente (
	customer_address_id INTEGER PRIMARY KEY,
	customer_id INTEGER NOT NULL,
	address_id INTEGER NOT NULL,
	FOREIGN KEY(customer_id) REFERENCES cliente(customer_id),
	FOREIGN KEY(address_id) REFERENCES direccion(address_id)
);

CREATE TABLE IF NOT EXISTS direccion_empleado (
	employee_address_id INTEGER PRIMARY KEY,
	employee_id INTEGER NOT NULL,
	address_id INTEGER NOT NULL,
	FOREIGN KEY(employee_id) REFERENCES empleado(employee_id),
	FOREIGN KEY(address_id) REFERENCES direccion(address_id)
);

INSERT INTO direccion_cliente(customer_id, address_id)
	SELECT cliente.customer_id AS customer_id,
		direccion.address_id AS address_id
	FROM cliente CROSS JOIN direccion
	WHERE address_id BETWEEN 101 AND 300
	LIMIT 200;

INSERT INTO direccion_cliente(employee_id, address_id)
	SELECT empleado.employee_id AS employee_id,
		direccion.address_id AS address_id
	FROM empleado CROSS JOIN direccion
	WHERE address_id BETWEEN 301 AND 500
	LIMIT 200;

--- 8) Ampliar el alcance de la entidad cuenta para que identifique el tipo de la misma

BEGIN;

CREATE TABLE cuenta_actualizado (
	account_id INTEGER PRIMARY KEY,
	customer_id INTEGER NOT NULL,
    account_type_id INTEGER,
	balance INTEGER NOT NULL,
	iban TEXT NOT NULL,
    FOREIGN KEY(customer_id) REFERENCES cliente(customer_id),
	FOREIGN KEY(account_type_id) REFERENCES tipo_cuenta(typing_id)
);

INSERT INTO cuenta_actualizado SELECT * FROM cuenta;

DROP TABLE cuenta;

ALTER TABLE cuenta_actualizado RENAME TO cuenta;

COMMIT;

--- 9) Asignar un tipo de cuenta a cada registro de cuenta de forma aleatoria

UPDATE cuenta SET account_type_id = abs(random()) % 3 + 1;

--- 10) Corregir el campo employee_hire_date de la tabla empleado con la fecha en formato YYYY-MM-DD

UPDATE empleado SET employee_hire_date = substr(employee_hire_date, 7, 4) || '-' || substr(employee_hire_date, 4, 2) || '-' || substr(employee_hire_date, 1, 2);