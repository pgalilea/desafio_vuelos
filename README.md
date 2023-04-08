# Desafío Vuelos
- [Desafío Vuelos](#desafío-vuelos)
	- [Ejecución básica con docker](#ejecución-básica-con-docker)
		- [Construir la imagen de docker](#construir-la-imagen-de-docker)
		- [Iniciar el contenedor basado en la imagen](#iniciar-el-contenedor-basado-en-la-imagen)
		- [Verificar ejecución](#verificar-ejecución)
	- [Realizar prueba de estrés](#realizar-prueba-de-estrés)
		- [Conectarse al contenedor en ejecución](#conectarse-al-contenedor-en-ejecución)
		- [Ejecutar prueba de estrés utilizando wrk](#ejecutar-prueba-de-estrés-utilizando-wrk)


## Ejecución básica con docker
### Construir la imagen de docker

```sh
docker build -t pred_vuelos .
```

### Iniciar el contenedor basado en la imagen
Elegir un puerto que tenga disponible la máquina local (en el ejemplo 8081)
```sh
docker run -d --name vuelos_api -p 8081:80 pred_vuelos
```

### Verificar ejecución
En el navegador web, se puede acceder a la ruta http://127.0.0.1:8081/docs
Expandir el endpoint "/predict-delay" y darle al botón "Try it out". Luego, completar el cuerpo de la consulta y darle a "execute".


## Realizar prueba de estrés
### Conectarse al contenedor en ejecución
En una ventana de terminal ejecutar

```sh
docker container attach vuelos_api
```

### Ejecutar prueba de estrés utilizando wrk
Situarse en la carpeta `tests/stress` del proyecto
En otra ventana de terminal, ejecutar un test simple
```sh
docker run --rm -v `pwd`:/data williamyeh/wrk -d10s -c10 -s post.lua --latency http://host.docker.internal:8081/predict-delay
```

La salida debería verse similar a:

```
Running 10s test @ http://host.docker.internal:8081/predict-delay
  2 threads and 10 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   123.07ms  180.87ms   1.11s    92.59%
    Req/Sec    66.56     23.65   130.00     71.27%
  Latency Distribution
     50%   71.72ms
     75%   99.01ms
     90%  157.96ms
     99%    1.00s 
  1219 requests in 10.10s, 178.69KB read
Requests/sec:    120.73
Transfer/sec:     17.70KB
```

Las requests se verán reflejadas en logs del contenedor.
```
INFO:     172.17.0.1:60904 - "POST /predict-delay HTTP/1.1" 200 OK
INFO:     172.17.0.1:60916 - "POST /predict-delay HTTP/1.1" 200 OK
INFO:     172.17.0.1:60902 - "POST /predict-delay HTTP/1.1" 200 OK
...
```

Ahora, para realizar una prueba más exigente:

```sh
docker run --rm -v `pwd`:/data williamyeh/wrk -d45s -c50000 -s post.lua --latency http://host.docker.internal:8081/predict-delay
```

<!---
TODO: incluir salida de wrk
-->



