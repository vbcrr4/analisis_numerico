# Modo de uso

# 1. Crear entorno virtual
python -m venv venv

# 2. Activar (Windows)
venv\Scripts\activate

#    Activar (Linux/Mac)
source venv/bin/activate

# 3. Instalar librerías
pip install sympy numpy

# 4. Verificar instalación
pip list

# 5. Ejecutar tu script
python tu_codigo.py


# 📊 Programa de Propagación de Errores en Funciones Matemáticas

Este programa en **Python** permite analizar cómo se propagan las incertidumbres en funciones matemáticas que dependen de una o varias variables.  
Se utiliza principalmente en contextos de **física, ingeniería y laboratorio**, donde es necesario calcular el error asociado a una magnitud derivada de otras.

---

## ⚙️ Tecnologías utilizadas
- [Python 3](https://www.python.org/)  
- [Sympy](https://www.sympy.org/) → para el manejo de expresiones simbólicas, derivadas y simplificación algebraica.  
- [NumPy](https://numpy.org/) → para operaciones numéricas.  

---

## 📌 Funcionamiento general

1. **Ingreso de la función matemática**  
   El usuario introduce una función en términos de variables (ejemplo: `π*r^2`, `m*g*h`, `x^2 + y^2`).

2. **Identificación de variables**  
   El programa detecta automáticamente las variables presentes en la función.

3. **Ingreso de valores y sus incertidumbres**  
   - Para cada variable, se solicita su valor nominal.  
   - Luego, se pide la incertidumbre asociada (puede ingresarse como valor absoluto o en porcentaje, por ejemplo: `0.01` o `5%`).  

4. **Cálculos principales**  
   - Valor nominal de la función evaluada con los datos ingresados.  
   - Derivadas parciales de la función respecto a cada variable.  
   - Evaluación de las derivadas en los valores nominales.  
   - Cálculo de la contribución de cada variable al error total.  
   - Error total propagado (suma de contribuciones).  
   - Error relativo (%) y el intervalo de confianza.

5. **Resultados en pantalla**  
   El programa muestra:
   - Función reconocida.  
   - Variables y sus valores con incertidumbre.  
   - Derivadas parciales.  
   - Contribuciones individuales al error.  
   - Error total propagado.  
   - Resultado final con incertidumbre.  
   - Intervalo de confianza.  

6. **Exportación opcional**  
   Los resultados pueden guardarse en un archivo de texto (`resultados.txt`).  

7. **Limitaciones**

Limitaciones técnicas

Ingreso de funciones restringido

El usuario debe escribir la función en una forma que sympy pueda interpretar.

No admite notación matemática más libre (ejemplo: sen(x) en vez de sin(x)).

Número fijo de variables

El programa necesita que se especifiquen las variables de entrada manualmente.

Si una función tiene muchas variables, se complica el uso.

Errores no controlados

Si el usuario ingresa mal la función o una variable, el programa puede romperse sin dar un mensaje claro.

Modelo de propagación de errores

Usa expansión de Taylor de primer orden.

Esto significa que el cálculo de incertidumbres es válido solo para errores pequeños.

Si los errores son grandes, el resultado no será confiable.

🔹 Limitaciones de usabilidad

Interfaz en consola

Todo se hace en línea de comandos.

No hay interfaz gráfica ni reportes automáticos en tabla o gráfico.

Unidades no contempladas

El programa no maneja unidades físicas (m, kg, s, etc.), solo números.

Es el usuario quien debe cuidar la consistencia de las unidades.

Salida básica

El resultado es solo un texto con valor ± error.

No genera archivos (CSV, LaTeX, PDF) ni gráficos de error automáticamente.

---


# Integrantes 

Donozo marquez nehuen
                        Ing Informatica
Becerra valentin 

