import numpy as np
import pandas as pd

# Funciones para obtener muestra aleatoria de una descarga en Brandwatch

def obtener_muestra(df, num_tuits, margen):
    idx = np.random.choice(list(df.index),num_tuits+margen)
    return df.loc[idx,['Author', 'Url', 'Full Text']]

def guardar_muestra(df, path):
    writer = pd.ExcelWriter(path, engine = 'xlsxwriter')
    df.to_excel(writer,sheet_name='Hoja1', index = None)
    writer.save()
    print('Listo!')

# Funciones para generar el reporte de comunidades utilizando Gephi

def obtener_proporcion_cuentas(df, tipo='rel'):
    q = df.groupby('modularity_class').agg({'Id' : ['nunique']})
    if tipo == 'relativo':
        return (q / q.sum()).sort_values(by = ('Id', 'nunique'),ascending = False).head(10) * 100
    elif tipo == 'absoluto':
        return q.sort_values(by = ('Id', 'nunique'), ascending = False).head(10)
    else:
        print('Tipo "{}" no reconocido. Los valores permitidos son "relativo" y "absoluto".'.format(tipo))

def obtener_proporcion_contenido(df, tipo = 'rel'):
    q = df.groupby('modularity_class').agg({'weighted indegree' : ['sum']})
    if tipo == 'relativo':
        return (q / q.sum()).sort_values(by = ('weighted indegree', 'sum'),ascending = False).head(10) * 100
    elif tipo == 'absoluto':
        return q.sort_values(by=('weighted indegree','sum'),ascending=False).head(10)
    else:
        print('Tipo "{}" no reconocido. Los valores permitidos son "relativo" y "absoluto".'.format(tipo))

def obtener_cuentas_autoridad(df, comunidad, percentil, detalle = 'simple'):
    umbral = np.percentile(df['weighted indegree'],percentil)
    print('Seleccionando cuentas que han sido retuiteadas igual o más de {} veces.'.format(umbral))
    resultado = df[df['weighted indegree']>=umbral].query('modularity_class=={}'.format(comunidad)).sort_values('weighted indegree',ascending=False)
    if detalle == 'completo':
        return resultado
    elif detalle == 'simple':
        return resultado['Id'].values
    else:
        print('Detalle "{}" no reconicido. Los valores permitidos son "simple" y "completo".'.format(detalle))

# Función para generar el reporte de 50 tuits más compartidos por comunidad. Se necesita de un csv de Gephi y uno de Brandwatch

def generar_reporte_tuits_por_comunidad(df_bw, df_ge, comunidades, num_tuits):

    df_bw['Author'] = df_bw['Author'].str.lower()
    df_bw['Thread Author'] = df_bw['Thread Author'].str.lower()

    df1 = df_bw.merge(df_ge[['Id','modularity_class']],left_on='Thread Author',right_on='Id',how='inner')

    sheets = {}
    for com in comunidades:
        q = df1.query('modularity_class=='+str(com))
        q = q.groupby(['Thread Author','Thread Id']).agg({'Url':['count'],'Full Text':['first']})
        q.columns = ['number','text']
        q = q.reset_index().sort_values('number',ascending=False).head(num_tuits)
        q['url'] = 'http://twitter.com/'+q['Thread Author'].map(str)+'/status/'+q['Thread Id'].map(str)
        sheets[com] = q

    return sheets

def guardar_reporte_tuits_por_comunidad(sheets, path):
	writer = pd.ExcelWriter(path, engine='xlsxwriter')
	for i,key in enumerate(sheets.keys()):
		sheets[key].to_excel(writer,sheet_name='Comunidad '+str(i+1),index=None)
	writer.save()
	print('Listo!')

