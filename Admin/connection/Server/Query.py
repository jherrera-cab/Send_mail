def query_obligation(date_query):
    text="""
        SELECT		*
        FROM		data_sinfin.gestion
        WHERE		"ENTIDAD_ID" = 'NATURGY' AND ("ID_EFECTO" = ' SOLICITUD FACTURA CORREO' OR "ID_EFECTO" = 'TOTAL CORREO')  AND DATE("HISTORY_DATE") = '{}'
            """.format(date_query)
    return text