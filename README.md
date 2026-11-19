# Neuro Explorer

Web educativa para aprender neurociencia de forma visual.

- **Atlas 3D**: modelo interactivo del cerebro (lóbulos, áreas funcionales, estructuras profundas, tronco encefálico y cerebelo) con fichas de función, lesiones y datos clave.
- **Atlas**: además, ubicación y notas clínicas de cada estructura, links a los procesos donde aparece y un modo **Desafío** para encontrar estructuras en el modelo.
- **Procesos**: 12 lecciones animadas paso a paso (potencial de acción, sinapsis, reflejo rotuliano, vía visual, memoria, recompensa, estrés, miedo, lenguaje, sueño, dolor y movimiento voluntario) con preguntas de repaso. Las estructuras de cada lección abren su ficha en el atlas 3D.

Sitio estático: `index.html` + `data/brain.json` (Three.js desde CDN). Contenido con fines educativos.

## Créditos del modelo 3D

- Corteza: superficie de la plantilla ICBM 2009 (Copyright © McConnell Brain Imaging Centre, Montreal Neurological Institute, McGill University), en la versión `BrainMesh_ICBM152` distribuida con Surf Ice / NiiVue (BSD-2).
- Ganglios basales e hipotálamo: atlas subcortical CIT168 (Pauli, Nili & Tyszka, 2018, *Scientific Data*).
- Tálamo, hipocampo, amígdala, hipófisis, cuerpo calloso, cerebelo y tronco: formas esquemáticas ubicadas en coordenadas MNI.
- `data/brain.json` se genera desde las mallas originales; la clasificación en lóbulos y áreas es aproximada.

Diseño: Mapa Bianchi.
