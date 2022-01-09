# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 22:30:57 2022

@author: iorla
"""


#importamos pandas para trabajar con dataframes
import pandas as pd 
import seaborn as sns


print('Bienvenido usuario \n')
print('En el siguiente analisis se muestran los datos para la empresa de')
print('"Synergy Logistics" en donde se analizaran:\n')
print('* Las rutas mas demandadas de importacion y exportacion \n')
print('* Los medios de transporte mas utilizados \n')  
print('* EL valor total de las importaciones y exportaciones \n')

#%%

# llamamos a nuestro archivo csv y lo convertimos a dataframe
synergy_dataframe = pd.read_csv('synergy_logistics_database.csv', index_col=0,
                                encoding='utf-8', 
                                parse_dates=[4, 5])

# filtraremos los datos en exportaciones e importaciones 
exports = synergy_dataframe[synergy_dataframe['direction'] == 'Exports']
imports = synergy_dataframe[synergy_dataframe['direction'] == 'Imports']
#%%
def  primera_exportacion(datos,n):
    # filtraremos los datos en exportaciones e importaciones 
    exports = synergy_dataframe[synergy_dataframe['direction'] == 'Exports']

 
    # Separamos los valores de exportaciones e importaciones
    # mostraremos las rutas mas solicitadas independientemente del costo
    opcion1_exportacion = exports.groupby(by=['origin','destination',
                                                        'transport_mode'])
    op1_exportation = opcion1_exportacion.describe()['total_value']
    op1_exportation = op1_exportation.sort_values(by='count',ascending=False)
    
   
    return op1_exportation.head(n)
#%%
  # repetimos para la importacion
def primera_importacion(datos,n):
    imports = synergy_dataframe[synergy_dataframe['direction'] == 'Imports']
    opcion1_importacion = imports.groupby(by=['origin','destination',
                                              'transport_mode'])
    op1_importation = opcion1_importacion.describe()['total_value']
    op1_importation = op1_importation.sort_values(by='count',ascending=False)
    
    return op1_importation.head(n)
#%%
def  primera_flujo(datos,n):
    # Separamos los valores de exportaciones e importaciones
    # mostraremos las rutas mas solicitadas independientemente del costo
    primero_flujo = datos.groupby(by=['origin','destination',
                                                  'transport_mode']).sum()[
                                                'total_value'].reset_index()
    first_val = primero_flujo.sort_values(by='total_value',ascending=False)
    
   
    return first_val.head(n)
#%%
#seccion de graficos
#dependiendo del anio, se mostrara el grafico correspondiente

def graficos_part_2(date):
    date = int(date)
    if date == 2015:
        datos_fecha = synergy_dataframe[synergy_dataframe['year'] == '2015'].copy()
    elif date == 2016:
        datos_fecha = synergy_dataframe[synergy_dataframe['year'] == '2016'].copy()
    elif date == 2017:
        datos_fecha = synergy_dataframe[synergy_dataframe['year'] == '2017'].copy()
    elif date == 2018:
        datos_fecha = synergy_dataframe[synergy_dataframe['year'] == '2018'].copy()
    elif date == 2019:
        datos_fecha = synergy_dataframe[synergy_dataframe['year'] == '2019'].copy()
    elif date == 2020:
        datos_fecha = synergy_dataframe[synergy_dataframe['year'] == '2020'].copy()
    datos_fecha['month'] = datos_fecha['date'].dt.month
    datos_por_mes = datos_fecha.groupby(['month', 'transport_mode'])
    datos_por_mes.sum()
    datos_por_mes.count()['total_value']
    datos_por_mes.describe()
    serie = datos_por_mes.count()['total_value']
    ddd = serie.to_frame().reset_index()
    ddd = ddd.pivot('month', 'transport_mode', 'total_value')
    
    return sns.lineplot(data=ddd)
    

#%%

def sol_2(datos):
    rutas = datos.groupby('transport_mode').sum()['total_value'].reset_index()
    total_valor_rutas = rutas['total_value'].sum()
    rutas['Porcentaje'] = rutas['total_value']/total_valor_rutas 
    lista_de_rutas = rutas.sort_values(by='Porcentaje', ascending=False)
    
    return lista_de_rutas

#%%
def sol_3(df, p):
    pais_total_value = df.groupby('origin').sum()['total_value'].reset_index()
    total_value_for_percent = pais_total_value['total_value'].sum()
    pais_total_value['percent'] = 100 * pais_total_value['total_value'] / total_value_for_percent
    pais_total_value.sort_values(by='percent', ascending=False, inplace=True)
    pais_total_value['Frecuencia acumulada'] = pais_total_value['percent'].cumsum()
    lista_pequena = pais_total_value[pais_total_value['Frecuencia acumulada'] < p]
    
    return lista_pequena
#%%

# ponemos los resultados planteados por el problema inicial
res_1_imp = primera_importacion(synergy_dataframe,10)
res_1_exp = primera_exportacion(synergy_dataframe,10)
res_1_flux = primera_flujo(synergy_dataframe,10)
res_2 = sol_2(synergy_dataframe)
res_3 = sol_3(synergy_dataframe, 80)
# graf_1 = graficos_part_2(2015)
# graf_2 = graficos_part_2(2016)
# graf_3 = graficos_part_2(2017)
# graf_4 = graficos_part_2(2018)
# graf_5 = graficos_part_2(2019)
# graf_6 = graficos_part_2(2020)

# comenzamos con la primera opcion

print('Para el caso de las ruta mas demandadas de importacion y exportacion ')
print('tenemos los siguientes datos. \n')
print('Si analizamos las primeras impotaciones por la cantidad de estas ')
print('sin importar el valor de la misma, tendremos: \n')
print('             ***IMPORTACIONES***            ')
print(res_1_imp)

print('\n\nSi analizamos las primeras expotaciones por la cantidad de estas ')
print('sin importar el valor de la misma, tendremos: \n')
print('             ***EXPORTACIONES***            ')
print(res_1_exp)

print('\n\nSi analizamos las primeras importaciones y expotaciones por la cantidad de')
print('estas tomando en cuenta el valor de las mismas, tendremos: \n')
print('             ***VALORES TOTALES***            \n')
print(res_1_flux)

# ahora con la segunda
print('\n\n\n\n Para  la segunda opcion, mostramos el medio de transporte utilizado\n')
print('             ***MEDIOS DE TRANSPORTE MAS USADOS***            \n')
print(res_2)
# usando la funcion 'graficos_part_2' se obtiene un grafico de cada anio

#finalmente con la tercera
print('\n\n\n\n Para la tercera opcion, se muestra el siguiente comportamiento:\n')
print('***TOP PAISES QUE GENERAN AL 80% DEL VALOR DE IMPORTACIONES/EXPORTACIONES***\n')
print(res_3)

    
    
    