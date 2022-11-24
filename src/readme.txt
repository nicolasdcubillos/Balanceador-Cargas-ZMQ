--- Introducción a Sistemas Distribuidos
-- Proyecto G1 : Esteban Alberto Rojas Molina
                 Angello Mateo Jaimes Rincón
                 Nicolás David Cubillos Cubillos

Para correr el código, primero hacer los ajustes necesarios dentro de los tres archivos (.py) para indicar las direcciones
de las máquinas en las cuales se van a instanciar los ejecutables.

- Crear instancias del servidor:
py Server.py ID

De esta manera se puede ejecutar los servidores que sean necesarios, teniendo en cuenta que por el ID que se indique en el
args de la ejecución, será el que identificará al servidor para las debidas peticiones entre el load balancer y este.

- Crear instancia del load balancer:
py LoadBalancer.py

- Crear instancia de los clientes:
py Client.py

Se pueden crear los clientes que se deseen. Cada que se inicie un cliente, se le otorogará un número como identificador de este
usado como tópico para las respuestas que se le entreguen a este.