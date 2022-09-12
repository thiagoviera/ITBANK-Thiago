--- 1) Seleccionar las cuentas con saldo negativo

SELECT * 
    FROM cuenta 
    WHERE balance < 0;

--- 2)Seleccionar el nombre, apellido y edad de los clientes que tengan en el apellido la letra Z

SELECT customer_name, customer_sunarme, dob 
    FROM cliente 
    WHERE instr(customer_surname, 'z') > 0 OR instr(customer_surname, 'Z');

--- 3)Seleccionar el nombre, apellido, edad y nombre de sucursal de las personas cuyo nombre sea “Brendan” y el resultado ordenarlo por nombre de sucursal

SELECT cliente.customer_name, cliente.customer_surname, CAST(strftime('%Y.%m%d', 'now') - strftime('%Y.%m%d', cliente.dob) AS INT) AS customer_age, sucursal.branch_name 
    FROM cliente, sucursal 
    WHERE customer_name = "Brendan" AND cliente.branch_id == sucursal.branch_id;

--- 4) Seleccionar de la tabla de préstamos, los préstamos con un importe mayor a $80.000 y los préstamos prendarios utilizando la unión de tablas/consultas 
--- (recordar que en las bases de datos la moneda se guarda como integer, en este caso con 2 centavos)

SELECT * 
    FROM prestamo 
    WHERE loan_total > 8000000
UNION
SELECT * 
    FROM prestamo
    WHERE loan_type == 'PRENDARIO';

--- 5) Seleccionar los prestamos cuyo importe sea mayor que el importe medio de todos los prestamos

SELECT * 
    FROM prestamo 
    WHERE loan_total > (SELECT AVG(loan_total) FROM prestamo);

--- 6) Contar la cantidad de clientes menores a 50 años

SELECT COUNT(*) 
    FROM cliente 
    WHERE dob > DATE('now', '-50 years');

--- 7) Seleccionar las primeras 5 cuentas con saldo mayor a 8.000$

SELECT * 
    FROM cuenta 
    WHERE balance > 800000
    LIMIT 5;

--- 8) Seleccionar los préstamos que tengan fecha en abril, junio y agosto, ordenándolos por importe

SELECT * 
    FROM prestamo
    WHERE substr(loan_date, 6, 2) == "04" OR substr(loan_date, 6, 2) == "06" OR substr(loan_date, 6, 2) == "08"
    ORDER BY loan_total DESC;

--- 9) Obtener el importe total de los prestamos agrupados por tipo de préstamos. Por cada tipo de préstamo de la tabla préstamo, calcular la suma de sus importes.
--- Renombrar la columna como loan_total_accu

SELECT loan_type, SUM(loan_total) AS loan_total_accu
    FROM prestamo
    GROUP BY loan_type;