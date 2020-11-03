from lifestore_file import lifestore_searches
from lifestore_file import lifestore_sales
from lifestore_file import lifestore_products
from lifestore_categories import product_categories

# Función contadora de búsquedas
def search_counter():
  def_counter = []
  for product_searches in lifestore_products:
    counter = 0
    for search in lifestore_searches:
      if search[1] == product_searches[0]:
        counter += 1

    def_counter.append([product_searches[3], counter])

  return def_counter

# Función contadora de ventas
def sales_counter(year, month):
  search_period = month + '/' + year
  #print('periodo de búsqueda: ' + month + '-' + year)
  def_counter = []
  for product in lifestore_products:
    counter = 0
    for sales in lifestore_sales:
      dt = sales[3]
      sales_date = dt[3:10]
      #print('sales_date' + sales_date)
      if sales[1] == product[0] and sales_date == search_period and sales[4] != 1:
        def_counter.append([product[1], product[2], product[3], sales[3]])

  return def_counter

def category_sales():
  # Menú de opciones
  years = ['2019', '2020']
  months = ['01','02','03','04','05','06','07','08','09','10','11','12']
  year = 0
  month = 0

  while year not in years:
    print("""SELECCIONE AÑO
    2020
    2019""")
    year = input("Seleccione el año: ")
  while month not in months:
    print("""\nMes en formato de dos dígitos (01, 09, 11, etc)
    """)
    month = input("Mes: ")
    sales = sales_counter(year,month)
    print('\n')

  unordered_category_sales = []
  for category in product_categories:
    counter = 0
    for product in lifestore_products:
      if product[3] == category:
        for prod_sales in sales:
          if prod_sales[0] == product[1]:
            counter += 1
        unordered_category_sales.append([category, product[1], counter])
  print('PERIODO: ' + str(month) + '-' + str(year))
  return unordered_category_sales

def category_sum():
  #Sumarizar por categoría
  counter = 0
  category_searches_list = []
  category = ''

  for cat_counter in searches_counter:
    if not category:
      category = cat_counter[0]
      counter = cat_counter[1]
    elif cat_counter[0] == category:
      counter += cat_counter[1]
    else:
      category_searches_list.append([category, counter])
      category = cat_counter[0]
      counter = cat_counter[1]

  """
  Para la última categoría de la lista, porque ya no entra a la comparación del loop pero si tiene la cuenta de las búsquedas
  """
  category_searches_list.append([category, counter])

  return category_searches_list

# Inicio main
# Lista de usuarios autorizados
admin_list = [["javier", "123"], ["pedro", "456"], ["daniel", "789"]]

# Variables de logueo
login_attempts = 0;
login_credentials = []

# Proceso de logueo
while login_credentials not in admin_list:
  if login_attempts >= 3:
    print("Ha intentado loguearse demasiadas veces. El acceso ha sido bloquedo")
    break
  elif login_attempts >= 1:
    print("Su nombre de usuario o contraseña no son correctos. Por favor, intente de nuevo")

  username = input("Ingrese su nombre de usuario: ")
  userpwd = input("Ingrese su contraseña: ")
  login_credentials = [username, userpwd]
  login_attempts += 1

if login_credentials in admin_list:
  print("Bienvenido!\n")
else:
  print("Si tiene problemas para acceder, contacte al administrador del sistema.")

continue_program = True
while continue_program == True:
  # Menú de opciones
  options = [1, 2, 3, 4, 5, 6, 7] #Se usa en el while del menú. Si el dato ingresado no existe en la lista, sigue mostrando el menú hasta que se seleccione una opción válida
  option = 0 # Se requiere un valor inicial para el while

  while option not in options:
    print("""MENU DE OPCIONES
    1. Productos con mayores ventas
    2. Producto con menores ventas
    3. Categorías más buscadas
    4. Categorías menos buscadas
    5. Productos con mejores reseñas
    6. Productos con peores reseñas
    7. Reporte de ventas por año""")
    option = int(input("Seleccione su opción: "))
    #Verificar si la respuesta se puede convertir a entero o repetir las opciones
    try:
      option = int(option)
    except ValueError:
      option = 0

  # OPCION 1 mayores ventas
  if option == 1:
    unordered_category_sales = category_sales()
    #Ordenamiento de mayor a menor de la lista
    ordered_category_sales = []
    while unordered_category_sales:
      for category in product_categories:
        max_searched = unordered_category_sales[0][2]
        current_max = [unordered_category_sales[0][0], unordered_category_sales[0][1], unordered_category_sales[0][2]]

        for product in unordered_category_sales:
          if product[2] > max_searched:
            max_searched = product[2]
            current_max = [product[0], product[1], product[2]]

        ordered_category_sales.append(current_max)
        unordered_category_sales.remove(current_max)

    #Salida de datos solicitado
    print('PRODUCTOS CON MAYORES VENTAS')
    print('No. VENTAS\t|| PRODUCTO')
    for index in range(50):
      print(str(ordered_category_sales[index][2]) + '        \t|| ' + ordered_category_sales[index][1])

  # OPCION 2 menores ventas
  if option == 2:
    unordered_category_sales = category_sales()
    #Ordenamiento de mayor a menor de la lista
    ordered_category_sales = []
    while unordered_category_sales:
      for category in product_categories:
        min_searched = unordered_category_sales[0][2]
        current_min = [unordered_category_sales[0][0], unordered_category_sales[0][1], unordered_category_sales[0][2]]

        for product in unordered_category_sales:
          if product[2] < min_searched:
            min_searched = product[2]
            current_min = [product[0], product[1], product[2]]

        ordered_category_sales.append(current_min)
        unordered_category_sales.remove(current_min)

    #Salida de datos solicitado
    print('PRODUCTOS CON MENORES VENTAS')
    print('No. VENTAS\t|| PRODUCTO')
    for index in range(50):
      print(str(ordered_category_sales[index][2]) + '        \t|| ' + ordered_category_sales[index][1])

  # OPCION 3 categorías más buscadas
  elif option == 3:
    """Contar el número de búsquedas para cada categoría"""
    #Sacar los totales por producto
    searches_counter = search_counter()

    #Sumarizar las búsquedas por categoría
    category_searches_list = category_sum()

    #Ordenar las búsquedas de mayor a menor
    ordered_list = []
    while category_searches_list:
      max_searched = category_searches_list[0][1]
      current_max = [category_searches_list[0][0], category_searches_list[0][1]]

      for category_listing in category_searches_list:
        if category_listing[1] > max_searched:
          max_searched = category_listing[1]
          current_max = [category_listing[0], category_listing[1]]

      ordered_list.append(current_max)
      category_searches_list.remove(current_max)

    #Imprimir el listado ordenado al usuario
    print("\nCategorías más buscadas")
    print('No. BUSQUEDAS\t|| CATEGORIA')
    for index in range(5):
      print(str(ordered_list[index][1]) + '           \t|| ' + ordered_list[index][0])


  # OPCION 4 categorías menos buscadas
  elif option == 4:
    """Contar el número de búsquedas para cada categoría"""
    #Sacar los totales por producto
    searches_counter = search_counter()

    #Sumarizar las búsquedas por categoría
    category_searches_list = category_sum()

    #Ordenar las búsquedas de mayor a menor
    ordered_list = []
    while category_searches_list:
      min_searched = category_searches_list[0][1]
      current_min = [category_searches_list[0][0], category_searches_list[0][1]]

      for category_listing in category_searches_list:
        if category_listing[1] < min_searched:
          min_searched = category_listing[1]
          current_min = [category_listing[0], category_listing[1]]

      ordered_list.append(current_min)
      category_searches_list.remove(current_min)

    #Imprimir el listado ordenado al usuario
    print("\nCategorías menos buscadas")
    print('No. BUSQUEDAS\t|| CATEGORIA')
    for index in range(5):
      print(str(ordered_list[index][1]) + '           \t|| ' + ordered_list[index][0])

  # OPCION 5 Mejores reseñas
  elif option == 5:
    #reviews = lifestore_sales
    reviews = []
    #Ordenar las reseñas de mayor a menor
    ordered_list = []
    remove_item = []
    for product in lifestore_products:
      # Usamos estas dos variables para sacar promedio de valoraciones por producto
      prod_review_sum = 0
      prod_review_count = 0
      for sales in lifestore_sales:
        if product[0] == sales[1] and sales[4] != 1:
          prod_review_sum += sales[2]
          prod_review_count += 1
      # Promedio de valoraciones
      if prod_review_count == 0:
        prod_review_avg = 0
      else:
        prod_review_avg = int(prod_review_sum/prod_review_count)

      reviews.append([product[1], prod_review_avg])

    while reviews:
      max_review = reviews[0][1]
      current_best = [reviews[0][0], reviews[0][1]]
      remove_item = reviews[0]

      for review_listing in reviews:
        if review_listing[1] > max_review:
          max_review = review_listing[1]
          current_best = [review_listing[0], review_listing[1]]
          remove_item = review_listing

      ordered_list.append(current_best)
      reviews.remove(remove_item)

    #Imprimir el listado ordenado al usuario
    print('PROM RESEÑAS\t|| PRODUCTO')
    for index in range(20):
      print('          ' + str(ordered_list[index][1]) +' \t|| ' + ordered_list[index][0])

  elif option == 6:
    #reviews = lifestore_sales
    reviews = []
    #Ordenar las reseñas de mayor a menor
    ordered_list = []
    remove_item = []
    for product in lifestore_products:
      # Usamos estas dos variables para sacar promedio de valoraciones por producto
      prod_review_sum = 0
      prod_review_count = 0
      for sales in lifestore_sales:
        if product[0] == sales[1] and sales[4] != 1:
          prod_review_sum += sales[2]
          prod_review_count += 1
      # Promedio de valoraciones
      if prod_review_count == 0:
        prod_review_avg = 0
      else:
        prod_review_avg = int(prod_review_sum/prod_review_count)

      reviews.append([product[1], prod_review_avg])

    while reviews:
      min_review = reviews[0][1]
      current_min = [reviews[0][0], reviews[0][1]]
      remove_item = reviews[0]

      for review_listing in reviews:
        if review_listing[1] < min_review:
          min_review = review_listing[1]
          current_min = [review_listing[0], review_listing[1]]
          remove_item = review_listing

      ordered_list.append(current_min)
      reviews.remove(remove_item)

    #Imprimir el listado ordenado al usuario
    print('PROM RESEÑAS\t|| PRODUCTO')
    for index in range(20):
      print('          ' + str(ordered_list[index][1]) +' \t|| ' + ordered_list[index][0])

  elif option == 7:
    years = ['2019', '2020']
    months = [['01', 'Ene'], ['02', 'Feb'], ['03', 'Mar'], ['04', 'Abr'], ['05', 'May'], ['06', 'Jun'], ['07', 'Jul'], ['08', 'Ago'], ['09', 'Sep'], ['10', 'Oct'], ['11', 'Nov'], ['12', 'Dic']]

    for year in years:
      month_sales = [] # Lista sin ordenar de ventas por mes
      ordered_mo_sales = [] # Lista ordenada de mayor a menor de ventas por mes
      yr_sales = 0
      print('VENTAS AÑO ' + year)
      for month in months:
        mo_sales = 0 # Ventas del mes
        sales = sales_counter(year, month[0])
        for period_sales in sales:
          product = period_sales[0]
          for price in lifestore_products:
            if price[1] == product:
              ppt = price[2]
              break
          mo_sales += ppt
        print('\t\t' + month[1] + '     \t| ' + str(mo_sales) + '.00')

        month_sales.append([month[1], mo_sales])
        yr_sales += mo_sales
      print('\t\t-----------------------------------')
      print('\t\tTOTAL     \t| ' + str(yr_sales) + '.00')
      """ PROMEDIO MENSUAL POR AÑO """
      mo_avg = yr_sales/12
      print('\t\t-----------------------------------')
      print('\t\tPROM MENSUAL| ' + str(mo_avg) + '\n')
      print('-------------------------------')

      # Meses con más ventas
      while month_sales:
        max_sales = month_sales[0][1]
        current_max = [month_sales[0][0], max_sales]

        for current_sale in month_sales:
          if current_sale[1] > max_sales:
            max_sales = current_sale[1]
            current_max = [current_sale[0], max_sales]

        ordered_mo_sales.append(current_max)
        month_sales.remove(current_max)

      print('\tMESES CON MEJORES VENTAS')
      for order in ordered_mo_sales:
        if order[1] > 0:
          print('\t' + order[0] + '     \t| ' + str(order[1]) + '.00')
      print('____________________________________\n')

  """
  Fin del reporte. Menú de Salida
  """
  valid_resp = [1, 2]
  resp = 0
  print('\nFIN DEL REPORTE')
  while resp not in valid_resp:
    print("""
    1. Continuar
    2. Salir
    """)
    resp = input("Seleccione su opción: ")
    #Verificar si la respuesta se puede convertir a entero o repetir las opciones
    try:
      resp = int(resp)
    except ValueError:
      resp = 0

    if int(resp) == 2:
      continue_program = False
      print('\n¡Hasta luego!')
