# 1. Usa una imagen ligera de Node 20
FROM node:20-alpine

# 2. Establece el directorio de trabajo
WORKDIR /usr/src/app

# 3. Copia primero los ficheros de dependencias para aprovechar el cache
COPY package.json package-lock.json ./

# 4. Instala las dependencias de producción y desarrollo
RUN npm ci

# 5. Copia el resto del código de la UI
COPY . .

# 6. Expón el puerto en el que corre Next.js
EXPOSE 3000

# 7. Comando por defecto: arranca en modo desarrollo
CMD ["npm", "run", "dev"]
