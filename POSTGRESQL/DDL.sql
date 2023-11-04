-- DDL
CREATE DABATASE lydemar;

create table ventas_tienda_productores (
	fecha  DATE,
	producto VARCHAR(40),
	cantidad integer,
	medida VARCHAR(20),
	precio_unitario numeric,
	precio_total numeric,
	cliente VARCHAR(50),
	timestamp TIMESTAMP
);

create table ventas_mayorista (
	id SERIAL primary KEY,
	fecha  DATE,
	cliente VARCHAR(100),
	tipo_de_documento VARCHAR(40),
	numero_documento VARCHAR (40),
	producto VARCHAR(40),
	cantidad integer,
	tipo_medida VARCHAR(20),
	precio_unitario numeric,
	precio_total numeric,
	timestamp TIMESTAMP
);
CREATE TABLE cobranzas (
	id SERIAL PRIMARY KEY,
	fecha DATE,
	numero_documento VARCHAR (40),
	monto NUMERIC,
	timestamp TIMESTAMP
)