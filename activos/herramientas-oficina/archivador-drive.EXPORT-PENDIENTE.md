# Export pendiente — Archivador Drive

El workflow `[ACTIVO] Archivador Drive` (26 nodos) está operativo en n8n y
probado, pero su export JSON completo aún no se subió a este repositorio.

## Cómo obtenerlo

1. Abrir el workflow en n8n:
   `https://studio-julio.duckdns.org/workflow/2bgdkH6nW4EtnEQw`
2. Menú `...` (arriba a la derecha) → **Download**.
3. Guardar el archivo como `archivador-drive.json` en esta misma carpeta.
4. Antes de commitear, **reemplazar el ID de la credencial de Drive** por el
   placeholder `"id": "REEMPLAZAR"` en los 5 nodos de Google Drive
   (Buscar Anio, Crear Anio, Buscar Mes, Crear Mes, Buscar Cliente,
   Crear Cliente, Subir Archivo).

## Estructura, por si hay que reconstruirlo

Patrón repetido por cada nivel de la ruta (año → mes → cliente), 6 nodos por
nivel:

```
Buscar <nivel>      Google Drive / fileFolder / search
                    queryString: {{ $json.<nivel> }}
                    filter.folderId: carpeta padre, whatToSearch: folders
                    alwaysOutputData: true
Resolver <nivel>    Code: busca coincidencia exacta de nombre en los
                    resultados; devuelve { existe, carpeta_actual } + contexto
Existe <nivel>?     IF sobre {{ $json.existe }} (boolean true)
  ├ true  → <nivel> Existente   Code: copia carpeta_actual → carpeta_<nivel>
  └ false → Crear <nivel>       Google Drive / folder / create
            → <nivel> Creado     Code: toma el id creado → carpeta_<nivel>
Nivel <nivel>       Merge (mode: append) — une ambas ramas
```

Cierre del flujo:

```
Nivel Cliente → Convertir Archivo (convertToFile / toBinary,
                sourceProperty: contenido_b64, dataIsBase64: true)
              → Subir Archivo (Drive / file / upload,
                folderId: carpeta_cliente)
              → Salida (Code: { ok, file_id, nombre, carpeta_id, ruta })
```

Entrada y normalización:

```
Entrada (webhook POST /archivador-drive, responseMode: lastNode)
  → Normalizar (Code): valida contenido_b64 y nombre_archivo;
    aplica defaults raiz='root', anio=año actual, mes=mes actual (2 dígitos),
    cliente='general', mime='application/octet-stream'
```

Los parámetros de entrada y la respuesta están documentados en el README de
esta carpeta.
