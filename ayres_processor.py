import pandas as pd
import glob
import os

def analizar_red_ayres():
    base_path = os.path.dirname(__file__)
    path = os.path.join(base_path, "reportes_ayres")
    archivos = glob.glob(os.path.join(path, "*.csv"))
    
    if not archivos:
        return pd.DataFrame()

    lista_sucursales = []

    for archivo in archivos:
        nombre_archivo = os.path.basename(archivo)
        try:
            # Leemos con el separador que confirmaste ';'
            df = pd.read_csv(archivo, sep=';', engine='python', encoding='latin1', on_bad_lines='skip')
            df.columns = [c.strip().lower() for c in df.columns]

            if 'total' in df.columns:
                # Limpiamos los números por si tienen puntos de miles o comas decimales
                for col in ['total', 'cantidad']:
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col].astype(str).str.replace('.', '').str.replace(',', '.'), errors='coerce')
                
                venta_total = df['total'].sum()
                unidades = df['cantidad'].sum() if 'cantidad' in df.columns else 0
                
                # Usamos el nombre de la sucursal que venga en el archivo o el nombre del archivo
                nombre_local = df['sucursal'].iloc[0] if 'sucursal' in df.columns else nombre_archivo

                lista_sucursales.append({
                    "Sucursal": str(nombre_local).upper(),
                    "Ventas $": float(venta_total),
                    "Unidades": int(unidades),
                    "Ticket Prom": float(venta_total / unidades) if unidades > 0 else 0
                })
        except Exception as e:
            print(f"Error en {nombre_archivo}: {e}")

    return pd.DataFrame(lista_sucursales)

# --- ESTA PARTE ESTABA DANDO EL ERROR DE ESPACIOS ---
if __name__ == "__main__":
    print("--- INICIANDO PRUEBA DE LECTURA ---")
    resultado = analizar_red_ayres()
    if resultado.empty:
        print("❌ Resultado vacío: No se encontraron datos o archivos.")
        # Verificación extra de ruta
        ruta_test = os.path.join(os.path.dirname(__file__), "reportes_ayres")
        print(f"Buscando en: {ruta_test}")
        if os.path.exists(ruta_test):
            print(f"Contenido de la carpeta: {os.listdir(ruta_test)}")
        else:
            print("LA CARPETA NO EXISTE EN ESTA RUTA.")
    else:
        print("✅ ¡DATOS ENCONTRADOS!")
        print(resultado)