-- todas las ventas del mes seleccionado que entran para el cálculo de las comisiones de aldair

WITH Total_Cobrado_Documento AS (
    SELECT 
        c.numero_documento,
        SUM(c.monto) AS total_cobrado
    FROM cobranzas c
    GROUP BY c.numero_documento
),
Cobros_Ultimos_Octubre AS (
    SELECT 
        c.numero_documento,
        MAX(c.fecha) AS ultima_fecha_cobro
    FROM cobranzas c
    WHERE DATE_TRUNC('month', c.fecha) = '2024-10-01'
    GROUP BY c.numero_documento
),
Ventas_Vendedor_Aldair AS (
    SELECT 
        v.numero_documento,
        v.cliente,
        SUM(v.precio_total) AS total_venta
    FROM ventas_mayorista v
    WHERE 
        v.vendedor = 'Aldair'
    GROUP BY v.numero_documento, v.cliente
),
Ventas_a_comisionar as (
SELECT 
    v.numero_documento,
    v.cliente,
    v.total_venta,
    t.total_cobrado
FROM Ventas_Vendedor_Aldair v
JOIN Total_Cobrado_Documento t 
    ON v.numero_documento = t.numero_documento
JOIN Cobros_Ultimos_Octubre c_oct
    ON v.numero_documento = c_oct.numero_documento
WHERE 
    v.total_venta = t.total_cobrado
order by numero_documento asc   
)
select
	fecha as fecha_venta,
	cliente,
	numero_documento,
	producto,
	precio_total
from ventas_mayorista
where numero_documento  in (select distinct numero_documento  from Ventas_a_comisionar )
order by numero_documento asc, producto asc
