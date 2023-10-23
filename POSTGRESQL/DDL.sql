-- DDL
create table ventas_tienda_productores (
	fecha  DATE,
	producto VARCHAR(40),
	cantidad integer,
	medida VARCHAR(20),
	precio_unitario numeric,
	precio_total numeric,
	cliente VARCHAR(50),
	timestamp TIMESTAMP
)
