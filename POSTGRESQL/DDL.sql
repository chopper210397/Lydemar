-- DDL
CREATE DABATASE lydemar;

create table ventas_mayorista (
	id SERIAL primary KEY,
	fecha  DATE,
	cliente VARCHAR(100),
	tipo_de_documento VARCHAR(40),
	numero_documento VARCHAR (40),
	producto VARCHAR(200),
	cantidad integer,
	tipo_medida VARCHAR(20),
	precio_unitario numeric,
	precio_total numeric,
	timestamp TIMESTAMP,
	vendedor VARCHAR(100),
	ubicacion VARCHAR(100)
);
CREATE TABLE cobranzas (
	id SERIAL PRIMARY KEY,
	fecha DATE,
	tipo_de_documento VARCHAR(80),
	numero_documento VARCHAR (40),
	medio_pago VARCHAR (80),
	monto NUMERIC,
	timestamp TIMESTAMP
);
CREATE TABLE products (
	id SERIAL PRIMARY KEY,
	product_name VARCHAR (100)
);
CREATE VIEW master_numero_documento AS
    select
    	distinct numero_documento
    FROM public.ventas_mayorista
    order by numero_documento 
;
create view master_ventas_cobranzas as
-- t1 = cobro por documento
with t1 as (
	select 
		numero_documento ,
		sum(monto) cobro_total,
		max(fecha) fecha_ultimo_pago
	from public.cobranzas c 
	group by numero_documento 
	) ,
--t2 = venta por documento
t2 as (
	select 	
		numero_documento ,
		sum(precio_total) venta_total,
		min(fecha) fecha_venta
	from ventas_mayorista vm 
	group by numero_documento 
)
select 
	t2.numero_documento,
	t2.fecha_venta,
	t1.fecha_ultimo_pago,
	t2.venta_total,
	t1.cobro_total,
	t2.venta_total - coalesce(t1.cobro_total,0) as deuda_restante
from t2
left join t1 on t1.numero_documento=t2.numero_documento
order by t2.fecha_venta asc
;
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