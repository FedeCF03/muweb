# Archivos de descarga del cliente.
#
# Acá van los .zip pesados. NO se suben a git (están en .gitignore).
# Caddy los sirve en /downloads/... con soporte de rangos (descarga reanudable).
#
# Para publicar el cliente:
#   1. Copiá el .zip acá, por ejemplo:  downloads/cliente-s6.zip
#   2. En content/downloads.yml poné  file: "cliente-s6.zip"  y  available: true
#   3. Calculá el sha256 y ponelo en el mismo YAML:
#        sha256sum downloads/cliente-s6.zip
#   4. Recargá la página: no hace falta reiniciar nada.
#
# Ojo: el zip que tenés en ~/MuOnline/Files S6.zip contiene el cliente Y el
# server. Subí solo la carpeta del cliente ("Cliente S6 Eng"), sin archivos
# del server ni el ServerInfo apuntando a otra IP.
