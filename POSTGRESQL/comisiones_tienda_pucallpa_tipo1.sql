-- monto de ventas por día realizada por la vendedora
create or replace view comisiones_tienda_pucallpa_tipo1 AS
with t1 as (
	select 
		date,
		sum("totalPrice") venta_diaria
	from ventas_tienda_mercado_mayorista_pucallpa vtmmp 
	where date not in ('2024-05-19','2024-05-20','2024-05-21','2024-05-22') -- quitamos los días que no trabajó priscila
	group by date
	order by date desc
),-- solo los dias que vendió mas de 1000 porque solo en esos cobra comisión
t2 as (
	select 	
		*
	from t1
	where venta_diaria > 1000
),-- calcula la comisión por día
t3 as (
	select 
		date,
		date_trunc('month',date::date)::date  mes,
		venta_diaria,
		(venta_diaria - 1000)*(0.5/100) "Comisión 0.5 %",
		(venta_diaria - 1000)*(0.8/100) "Comisión 0.8 %",
		(venta_diaria - 1000)*(1.0/100) "Comisión 1 %",
		(venta_diaria - 1000)*(1.2/100) "Comisión 1.2 %",
		(venta_diaria - 1000)*(1.5/100) "Comisión 1.5 %",
		(venta_diaria - 1000)*(1.8/100) "Comisión 1.8 %",
		(venta_diaria - 1000)*(2.0/100) "Comisión 2 %"
	from t2
), -- calcula la comisión mensual
t4 as (
	select
		mes,
		round(sum("Comisión 0.5 %")) "Comisión 0.5 %",
		round(sum("Comisión 0.8 %")) "Comisión 0.8 %",
		round(sum("Comisión 1 %")) "Comisión 1 %",
		round(sum("Comisión 1.2 %")) "Comisión 1.2 %",
		round(sum("Comisión 1.5 %")) "Comisión 1.5 %",
		round(sum("Comisión 1.8 %")) "Comisión 1.8 %",
		round(sum("Comisión 2 %")) "Comisión 2 %"
	from t3
	group by mes
	order by mes desc
)
select 
	*
from t4