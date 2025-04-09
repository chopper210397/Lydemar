CREATE OR REPLACE VIEW stock_leoncio_prado_actualizado_view as 
with salidas_por_dia_despues_stock_table as (
select
	producto ,
	tipo_medida ,
	SUM(cantidad) AS cantidad_vendida
from ventas_mayorista vm 
where fecha > (select max(fecha) from leoncio_prado_products_stock_table)::date
group by producto ,tipo_medida 
order by producto asc
)
select
	lppst."NOMBRE",
	lppst."PRESENTACION",
	lppst."STOCK  ACTUAL"::numeric as stock_inicial,
	coalesce(spddst.cantidad_vendida::numeric,0) as cantidad_vendida,
	(lppst."STOCK  ACTUAL"::numeric - coalesce(spddst.cantidad_vendida::numeric,0)) as stock_al_dia,
	lppst.fecha as fecha_conteo_stock
from leoncio_prado_products_stock_table lppst
left join salidas_por_dia_despues_stock_table spddst on lppst."NOMBRE" = spddst.producto and lower(lppst."PRESENTACION") = lower(spddst.tipo_medida)
order by lppst."NOMBRE" asc