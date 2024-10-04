create or replace view comisiones_tienda_pucallpa_tipo2 AS
WITH VentasDiarias AS (
    -- Paso 1: Calcular el total acumulado de ventas por cada producto según el orden de registro
    SELECT
        date("dateRegister") AS Fecha,
        "productName",
        "dateRegister",
        "totalPrice",
        SUM("totalPrice") OVER (PARTITION BY date("dateRegister") ORDER BY "dateRegister") AS Acumulado
    FROM ventas_tienda_mercado_mayorista_pucallpa
),
VentasComisionables AS (
    -- Paso 2: Identificar el punto donde se superan los 1000 soles
    SELECT
        Fecha,
        "productName",
        "totalPrice",
        Acumulado,
        "dateRegister",
        CASE
            WHEN Acumulado - "totalPrice" < 1000 AND Acumulado >= 1000 THEN Acumulado - 1000  -- Si la venta actual cruzó el umbral de 1000 soles
            WHEN Acumulado >= 1000 THEN "totalPrice" -- Si todas las ventas de este registro son comisionables
            ELSE 0 -- Si el acumulado no ha superado los 1000 soles
        END AS Comisionable
    FROM VentasDiarias
),
ComisionesCalculadas AS (
    -- Paso 3: Calcular la comisión basada en el tipo de producto y el monto comisionable
    SELECT
        Fecha,
        "productName",
        Comisionable,
        CASE
            WHEN "productName" LIKE ('GELATINA%') THEN 0.005
            WHEN "productName" LIKE ('FLAN%') THEN 0.005
            WHEN "productName" LIKE ('MAZAMORRA%') THEN 0.005
            WHEN "productName" LIKE ('LAVAVAJILLA LESLI%') THEN 0.005
            WHEN "productName" LIKE ('%ÑAPANCHA%') THEN 0.005
            WHEN "productName" LIKE ('DETERGENTE%') THEN 0.005
            WHEN "productName" LIKE ('PILLCO MOZO%') THEN 0.000
            WHEN "productName" LIKE ('PILLCO REY%') THEN 0.000
            WHEN "productName" LIKE ('ACEITE%') THEN 0.000
            WHEN "productName" LIKE ('SHAMPOO%') THEN 0.005
            WHEN "productName" LIKE ('BANQUITO RATAN%') THEN 0.005
            WHEN "productName" LIKE ('VELA%') THEN 0.005
            WHEN "productName" LIKE ('GRATED%') THEN 0.01
            WHEN "productName" LIKE ('OVAL%') THEN 0.01
            WHEN "productName" LIKE ('TINAPA%') THEN 0.01
            WHEN "productName" LIKE ('TINAPON%') THEN 0.01
            WHEN "productName" LIKE ('FILETE DE CABALLA%') THEN 0.01
            WHEN "productName" LIKE ('LAPICERO%') THEN 0.01
            WHEN "productName" LIKE ('ESPIRAL%') THEN 0.01
            WHEN "productName" LIKE ('ENCENDEDOR%') THEN 0.01
            WHEN "productName" LIKE ('PASTA DENTAL%') THEN 0.01
            WHEN "productName" LIKE ('LAVAVAJILLA QMASTER%') THEN 0.01
            WHEN "productName" LIKE ('LEJIA%') THEN 0.01
            WHEN "productName" LIKE ('%ATUN%') THEN 0.015
            WHEN "productName" LIKE ('%ATÚN%') THEN 0.015
            WHEN "productName" LIKE ('VINO%') THEN 0.02
            WHEN "productName" LIKE ('RON%') THEN 0.02
            WHEN "productName" LIKE ('LIMPIATODO%') THEN 0.02
            WHEN "productName" LIKE ('CIGARRO%') THEN 0.02
            ELSE 0.005 -- En caso de productos no listados, no hay comisión
        END AS TasaComision,
        Comisionable * CASE
            WHEN "productName" LIKE ('GELATINA%') THEN 0.005
            WHEN "productName" LIKE ('FLAN%') THEN 0.005
            WHEN "productName" LIKE ('MAZAMORRA%') THEN 0.005
            WHEN "productName" LIKE ('LAVAVAJILLA LESLI%') THEN 0.005
            WHEN "productName" LIKE ('%ÑAPANCHA%') THEN 0.005
            WHEN "productName" LIKE ('DETERGENTE%') THEN 0.005
            WHEN "productName" LIKE ('PILLCO MOZO%') THEN 0.000
            WHEN "productName" LIKE ('PILLCO REY%') THEN 0.000
            WHEN "productName" LIKE ('ACEITE%') THEN 0.000
            WHEN "productName" LIKE ('SHAMPOO%') THEN 0.005
            WHEN "productName" LIKE ('BANQUITO RATAN%') THEN 0.005
            WHEN "productName" LIKE ('VELA%') THEN 0.005
            WHEN "productName" LIKE ('GRATED%') THEN 0.01
            WHEN "productName" LIKE ('OVAL%') THEN 0.01
            WHEN "productName" LIKE ('TINAPA%') THEN 0.01
            WHEN "productName" LIKE ('TINAPON%') THEN 0.01
            WHEN "productName" LIKE ('FILETE DE CABALLA%') THEN 0.01
            WHEN "productName" LIKE ('LAPICERO%') THEN 0.01
            WHEN "productName" LIKE ('ESPIRAL%') THEN 0.01
            WHEN "productName" LIKE ('ENCENDEDOR%') THEN 0.01
            WHEN "productName" LIKE ('PASTA DENTAL%') THEN 0.01
            WHEN "productName" LIKE ('LAVAVAJILLA QMASTER%') THEN 0.01
            WHEN "productName" LIKE ('LEJIA%') THEN 0.01
            WHEN "productName" LIKE ('%ATUN%') THEN 0.015
            WHEN "productName" LIKE ('%ATÚN%') THEN 0.015
            WHEN "productName" LIKE ('VINO%') THEN 0.02
            WHEN "productName" LIKE ('RON%') THEN 0.02
            WHEN "productName" LIKE ('LIMPIATODO%') THEN 0.02
            WHEN "productName" LIKE ('CIGARRO%') THEN 0.02
            ELSE 0.005 -- En caso de productos no listados, no hay comisión
        END AS Comision
    FROM VentasComisionables
)
-- Paso final: Sumar la comisión total por día
SELECT
    date_trunc('month',Fecha)::date mes,
    round(SUM(Comision)) AS ComisionTotalMes
FROM ComisionesCalculadas
where Fecha not in ('2024-06-11','2024-06-12','2024-06-27','2024-06-28',
                    '2024-07-05','2024-07-22','2024-07-24'
                    ,'2024-08-11','2024-08-16','2024-08-17','2024-08-18') -- son fechas que priscila no trabajó, por ende no se le paga comisiones
GROUP BY mes
ORDER BY mes desc;
