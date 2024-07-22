def query_letter(date_query):
    text="""
        SELECT		A."ACCOUNT_NUMBER",
			A."ENTIDAD_ID",
			A."IDENTIFICACION",
			"GESTOR_ID",
			"HISTORY_DATE",
			"ID_ACCION",
			"ID_EFECTO",
			"OBSERVACION",
			"TELEPHONE",
			"REASON_ID",
			B."TEXT1",
			B."TEXT2",
			"MONEY1",
			A."TELEPHONE"
FROM		data_sinfin.gestion as a
INNER JOIN 	data_sinfin.obligaciones AS B ON A."ACCOUNT_NUMBER" = B."ACCOUNT_NUMBER"
WHERE		a."ENTIDAD_ID" = 'NATURGY' AND ("ID_EFECTO" = 'SOLICITUD FACTURA CORREO' OR "ID_EFECTO" = 'TOTAL CORREO' OR "ID_EFECTO" = 'PARCIAL CORREO')  AND DATE("HISTORY_DATE") = '{}' 
            """.format(date_query)
    return text