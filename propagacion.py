from sympy import *
import numpy as np
init_printing()

# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================
def ingresar_valor(mensaje, tipo=float):
    """Solicita un valor al usuario con validación"""
    while True:
        try:
            valor = input(mensaje)
            if valor.strip() == '':
                return None
            return tipo(valor)
        except ValueError:
            print("⚠️  Error: Por favor ingrese un valor numérico válido.")

def ingresar_incertidumbre(mensaje, valor_nominal, tipo=float):
    """Solicita incertidumbre con opción de porcentaje"""
    while True:
        entrada = input(mensaje)
        if entrada.strip() == '':
            return None
        
        if '%' in entrada:
            try:
                porcentaje = float(entrada.replace('%', '').strip())
                return abs(valor_nominal * porcentaje / 100)
            except ValueError:
                print("⚠️  Error: Porcentaje inválido.")
        else:
            try:
                return tipo(entrada)
            except ValueError:
                print("⚠️  Error: Ingrese un valor numérico o porcentaje.")

def parsear_funcion(expresion_str, variables):
    """Convierte string a expresión sympy"""
    try:
        # Reemplazar notación científica
        expresion_str = expresion_str.replace('^', '**')
        expresion_str = expresion_str.replace('e', 'E')
        
        # Parsear expresión
        expr = sympify(expresion_str)
        return expr
    except Exception as e:
        print(f"⚠️  Error al parsear la función: {e}")
        return None

def obtener_variables(expr):
    """Obtiene las variables de una expresión sympy"""
    return list(expr.free_symbols)

def evaluar_numericamente(expr, valores):
    """Evalúa una expresión sympy numéricamente"""
    try:
        # Convertir a float si es posible
        return float(expr.subs(valores))
    except:
        # Si no se puede convertir a float, mantener como expresión
        return expr.subs(valores)

# =============================================================================
# INTERFAZ PRINCIPAL
# =============================================================================
def main():
    print("🔧" + "="*70)
    print("           PROPAGACIÓN DE ERRORES EN FUNCIONES MATEMÁTICAS")
    print("="*70)
    
    while True:
        print("\n📝 INGRESE LA FUNCIÓN MATEMÁTICA")
        print("   Ejemplos:")
        print("   - F*L^4/(8*E*I)")
        print("   - m*g*h")
        print("   - π*r^2")
        print("   - 4/3*π*r^3")
        print("   - 2*π*sqrt(L/g)")
        print("   - x^2 + y^2 + sin(x*y)")
        print("\n💡 Use: + - * / ** ^ sin() cos() tan() exp() log() sqrt() pi E")
        
        # Ingresar función
        while True:
            funcion_str = input("\nIngrese la función (ej: π*r^2): ").strip()
            if funcion_str:
                break
            print("⚠️  La función no puede estar vacía.")
        
        # Parsear función
        expr = parsear_funcion(funcion_str, [])
        if expr is None:
            continue
        
        # Obtener variables
        variables = obtener_variables(expr)
        if not variables:
            print("⚠️  La función no contiene variables. Use letras como x, y, z, etc.")
            continue
        
        print(f"\n✅ Función reconocida: {expr}")
        print(f"📋 Variables detectadas: {[str(v) for v in variables]}")
        
        # Ingresar valores de variables
        valores_nominales = {}
        incertidumbres = {}
        
        print(f"\n📊 INGRESE VALORES PARA LAS VARIABLES:")
        for var in variables:
            nombre_var = str(var)
            valor = ingresar_valor(f"Valor de {nombre_var}: ")
            if valor is None:
                print(f"⚠️  Debe ingresar un valor para {nombre_var}")
                break
            
            # Solicitar incertidumbre
            inc = ingresar_incertidumbre(
                f"Incertidumbre Δ{nombre_var} (absoluta o %): ", 
                valor
            )
            if inc is None:
                print(f"⚠️  Debe ingresar incertidumbre para {nombre_var}")
                break
            
            valores_nominales[var] = valor
            incertidumbres[var] = inc
        
        if len(valores_nominales) != len(variables):
            continue
        
        # =============================================================================
        # CÁLCULOS
        # =============================================================================
        print("\n" + "🧮" + "="*60)
        print("                  REALIZANDO CÁLCULOS")
        print("="*60)
        
        # Calcular valor nominal (numéricamente)
        valor_nominal = evaluar_numericamente(expr, valores_nominales)
        
        # Calcular derivadas parciales y contribuciones al error
        contribuciones = {}
        error_total = 0
        
        for var in variables:
            # Derivada parcial
            derivada = expr.diff(var)
            derivada_eval = evaluar_numericamente(derivada, valores_nominales)
            
            # Contribución al error
            contribucion = abs(derivada_eval) * incertidumbres[var]
            contribuciones[var] = {
                'derivada': derivada,
                'derivada_eval': derivada_eval,
                'contribucion': contribucion
            }
            error_total += contribucion
        
        # =============================================================================
        # RESULTADOS
        # =============================================================================
        print("\n🎯" + "="*70)
        print("                         RESULTADOS")
        print("="*70)
        
        print(f"\n📈 FUNCIÓN: {expr}")
        print(f"\n📊 VALORES INGRESADOS:")
        for var in variables:
            nombre = str(var)
            print(f"   {nombre} = {valores_nominales[var]} ± {incertidumbres[var]}")
        
        print(f"\n✅ VALOR NOMINAL:")
        valores_str = ', '.join([f"{valores_nominales[v]}" for v in variables])
        print(f"   f({valores_str}) = {valor_nominal:.8g}")
        
        print(f"\n📐 DERIVADAS PARCIALES:")
        for var in variables:
            derivada = contribuciones[var]['derivada']
            derivada_eval = contribuciones[var]['derivada_eval']
            print(f"   ∂f/∂{var} = {derivada}")
            print(f"   ∂f/∂{var}|eval = {derivada_eval:.6g}")
        
        print(f"\n🔍 CONTRIBUCIONES AL ERROR:")
        for var in variables:
            contrib = contribuciones[var]['contribucion']
            porcentaje = (contrib / error_total * 100) if error_total != 0 else 0
            print(f"   Por {var}: {contrib:.6g} ({porcentaje:.1f}%)")
        
        print(f"\n⚠️  ERROR TOTAL PROPAGADO:")
        print(f"   Δf = ±{error_total:.8g}")
        
        print(f"\n🎯 RESULTADO FINAL:")
        print(f"   f = ({valor_nominal:.8g} ± {error_total:.8g})")
        
        if abs(valor_nominal) > 1e-10:  # Evitar división por cero
            error_relativo = (error_total / abs(valor_nominal)) * 100
            print(f"   Error relativo: {error_relativo:.2f}%")
        
        print(f"\n📏 INTERVALO DE CONFIANZA:")
        print(f"   [{valor_nominal - error_total:.8g}, {valor_nominal + error_total:.8g}]")
        
        # =============================================================================
        # OPCIONES ADICIONALES
        # =============================================================================
        exportar = input("\n💾 ¿Exportar resultados? (s/n): ").lower()
        if exportar in ['s', 'si', 'sí', 'y', 'yes']:
            nombre_archivo = input("Nombre del archivo (default: resultados.txt): ") or "resultados.txt"
            with open(nombre_archivo, 'a') as f:
                f.write("\n" + "="*50 + "\n")
                f.write(f"Función: {expr}\n")
                f.write("Variables:\n")
                for var in variables:
                    f.write(f"  {var} = {valores_nominales[var]} ± {incertidumbres[var]}\n")
                f.write(f"Resultado: {valor_nominal:.8g} ± {error_total:.8g}\n")
                f.write(f"Intervalo: [{valor_nominal - error_total:.8g}, {valor_nominal + error_total:.8g}]\n")
            print(f"✅ Resultados exportados a '{nombre_archivo}'")
        
        # Preguntar si desea realizar otro cálculo
        continuar = input("\n🔄 ¿Desea analizar otra función? (s/n): ").lower()
        if continuar not in ['s', 'si', 'sí', 'y', 'yes']:
            break
    
    print("\n" + "="*70)
    print("¡Gracias por usar el analizador de propagación de errores! 🎉")
    print("="*70)

# =============================================================================
# EJEMPLOS DE USO
# =============================================================================
def mostrar_ejemplos():
    print("\n📚 EJEMPLOS DE FUNCIONES COMUNES:")
    ejemplos = [
        ("Área círculo", "π*r^2"),
        ("Volumen esfera", "4/3*π*r^3"),
        ("Energía cinética", "0.5*m*v^2"),
        ("Período péndulo", "2*π*sqrt(L/g)"),
        ("Ley Ohm", "I*R"),
        ("Teorema Pitágoras", "sqrt(x^2 + y^2)"),
        ("Función trigonométrica", "sin(x) + cos(y)"),
        ("Exponencial", "A*exp(-k*t)"),
    ]
    
    for i, (nombre, formula) in enumerate(ejemplos, 1):
        print(f"{i}. {nombre}: {formula}")

# =============================================================================
# EJECUCIÓN
# =============================================================================
if __name__ == "__main__":
    mostrar_ejemplos()
    main()