from rich.console import Console
from rich.table import Table

console = Console()

def calcular_ganancia(precio_compra, precio_venta, monto_invertido, moneda="MXN", maker=False):
    # Comisiones según moneda y tipo de orden
    if moneda == "MXN":
        maker_fee = 0.005
        taker_fee = 0.0065
    elif moneda == "USD":
        maker_fee = 0.0025
        taker_fee = 0.003
    else:
        maker_fee = 0.005
        taker_fee = 0.0065

    fee = maker_fee if maker else taker_fee

    cantidad = monto_invertido / precio_compra
    comision_compra = monto_invertido * fee
    comision_venta = (precio_venta * cantidad) * fee
    costo_total = monto_invertido + comision_compra
    ingreso_total = (precio_venta * cantidad) - comision_venta
    ganancia = ingreso_total - costo_total
    porcentaje = (ganancia / costo_total) * 100
    ganancia_total = monto_invertido + ganancia

    return {
        "Moneda": moneda,
        "Cantidad de criptos": round(cantidad, 8),
        "Comisión compra": round(comision_compra, 2),
        "Comisión venta": round(comision_venta, 2),
        "Comisiones totales": round(comision_compra + comision_venta, 2),
        "Costo total": round(costo_total, 2),
        "Ingreso total": round(ingreso_total, 2),
        "Ganancia neta": round(ganancia, 2),
        "Ganancia %": round(porcentaje, 2),
        "Ganancia total": round(ganancia_total, 2)
    }

def calcular_precio_salida(precio_compra, monto_invertido, ganancia_deseada, moneda="MXN", maker=False):
    if moneda == "MXN":
        maker_fee = 0.005
        taker_fee = 0.0065
    elif moneda == "USD":
        maker_fee = 0.0025
        taker_fee = 0.003
    else:
        maker_fee = 0.005
        taker_fee = 0.0065

    fee = maker_fee if maker else taker_fee

    cantidad = monto_invertido / precio_compra
    comision_compra = monto_invertido * fee
    costo_total = monto_invertido + comision_compra
    precio_venta = (ganancia_deseada + costo_total) / (cantidad * (1 - fee))
    return round(precio_venta, 2)

def mostrar_tabla(resultado):
    tabla = Table(title="Resultados de Trading", title_style="bold underline", show_lines=True, header_style="bold magenta")
    tabla.add_column("Concepto", justify="center")
    tabla.add_column("Valor", justify="center")

    for k, v in resultado.items():
        if k in ["Precio de venta necesario", "Ganancia neta (esperada)", "Ganancia neta"]:
            color = "green"
        elif k in ["Comisión compra", "Comisión venta", "Comisiones totales"]:
            color = "red"
        elif k == "Ganancia total":
            color = "orange1"
        elif k == "Cantidad de criptos":
            color = "cyan"
        else:
            color = "white"
        tabla.add_row(k, f"[{color}]{v}[/{color}]")
    
    console.print(tabla, justify="center")

# === Programa principal ===
while True:
    print("\n=== Cálculo de Ganancia Bitso ===")
    print("1. XRP")
    print("2. ETH")
    print("3. LTC")
    print("4. USD")
    print("5. Predicción de precio de venta")
    print("6. Predicción sobre ganancia")
    print("7. Salir")

    criptos = {"1": "XRP", "2": "ETH", "3": "LTC", "4": "USD"}
    opcion = input("\nSelecciona una opción (1-7): ")

    if opcion == "7":
        print("\n✅ Saliendo del programa... ¡Hasta luego!")
        break

    if opcion in ["1","2","3","4","5","6"]:
        if opcion == "5":
            print("\nHas seleccionado: Predicción de precio de venta")
            for k,v in criptos.items():
                if k != "5":
                    print(f"{k}. {v}")
            sub_opcion = input("\nElige una criptomoneda o USD (1-4): ")
            if sub_opcion not in criptos or sub_opcion=="5":
                print("Opción inválida.")
            else:
                cripto = criptos[sub_opcion]
                moneda = "USD" if cripto=="USD" else "MXN"
                precio_compra = float(input(f"Precio de compra ({cripto}): "))
                precio_venta = float(input(f"Precio de venta ({cripto}): "))
                monto = float(input(f"Monto total invertido en {moneda}: "))
                tipo_orden = input("¿La orden será Maker (M) o Taker (T)? M ").strip().upper()
                if tipo_orden == "":
                    tipo_orden = "M"
                maker = tipo_orden == "M"
                resultado = calcular_ganancia(precio_compra, precio_venta, monto, moneda, maker)
                mostrar_tabla(resultado)

        elif opcion == "6":
            print("\nHas seleccionado: Predicción sobre ganancia")
            cripto = input("Nombre de la criptomoneda o USD: ").strip().upper()
            moneda_input = input("¿Operarás en USD? (Enter para MXN por defecto): ").strip().upper()
            moneda = "USD" if moneda_input == "USD" else "MXN"
            precio_compra = float(input(f"Valor de compra ({cripto}): "))
            monto = float(input(f"Cantidad a invertir en {moneda}: "))
            tipo_orden = input("¿La orden será Maker (M) o Taker (T)? M ").strip().upper()
            if tipo_orden == "":
                tipo_orden = "M"
            maker = tipo_orden == "M"
            precio_venta = calcular_precio_salida(precio_compra, monto, ganancia_deseada=0, moneda=moneda, maker=maker)
            tabla = Table(title="Predicción sobre ganancia", show_lines=True)
            tabla.add_column("Concepto", justify="center")
            tabla.add_column("Valor", justify="center")
            tabla.add_row("Valor de venta recomendado", f"[green]{precio_venta} {moneda}[/{'green'}]")
            console.print(tabla, justify="center")

        else:
            cripto = criptos[opcion]
            moneda_input = input("¿Operarás en USD? (Enter para MXN por defecto): ").strip().upper()
            moneda = "USD" if moneda_input == "USD" else "MXN"
            precio_compra = float(input(f"Precio de compra ({cripto}): "))
            precio_venta = float(input(f"Precio de venta ({cripto}): "))
            monto = float(input(f"Monto total invertido en {moneda}: "))
            tipo_orden = input("¿La orden será Maker (M) o Taker (T)? M ").strip().upper()
            if tipo_orden == "":
                tipo_orden = "M"
            maker = tipo_orden == "M"
            resultado = calcular_ganancia(precio_compra, precio_venta, monto, moneda, maker)
            mostrar_tabla(resultado)
    else:
        print("Opción inválida. Intenta nuevamente.")
