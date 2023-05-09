-- joining ventas and cobranzas table
select 
	c."Cliente" ,
	v."Fecha documento" ,
	--v."Sucursal" ,
	v."Tipo_documento" ,
	v."Fecha documento" ,
	v.document_number,
	v."Estado Doc." ,
	v."Importe" ,
	v."Total" ,
	c."Deuda Total" ,
	c."Abonos Total" 
from ventas v 
left join cobranzas c 
on v.document_number=c.document_number
where c.id is not null
