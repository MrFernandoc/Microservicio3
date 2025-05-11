# Etapa 1: Construcción del proyecto
FROM maven:3.9.6-eclipse-temurin-21 as builder
WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN mvn clean package -DskipTests

# Etapa 2: Imagen final
FROM eclipse-temurin:21-jdk-alpine
VOLUME /tmp
WORKDIR /app

# Copiamos el JAR desde la imagen builder
COPY --from=builder /app/target/labexamns-*.jar app.jar

# Exponer el puerto
EXPOSE 8080

# Comando para ejecutar la aplicación
ENTRYPOINT ["java", "-jar", "app.jar"]
