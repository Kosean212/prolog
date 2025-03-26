% Clientes
cliente(juan, "Juan Pérez", "juan@email.com", 5551234, "activo").
cliente(maria, "Maria López", "maria@email.com", 5555678, "inactivo").
cliente(carlos, "Carlos Díaz", "carlos@email.com", 5558765, "activo").
cliente(ana, "Ana Gómez", "ana@email.com", 5554321, "activo").

% Productos
producto(laptop, "Laptop HP", 1200, "Electrónica").
producto(mouse, "Mouse Logitech", 25, "Accesorios").
producto(teclado, "Teclado Mecánico", 80, "Accesorios").
producto(monitor, "Monitor 24 pulgadas", 250, "Electrónica").
producto(smartphone, "Smartphone Samsung", 700, "Electrónica").
producto(cargador, "Cargador USB-C", 15, "Accesorios").

% Vendedores
vendedor(ana, "Ana Torres", "ana@tienda.com").
vendedor(pedro, "Pedro Sánchez", "pedro@tienda.com").
vendedor(luis, "Luis Martínez", "luis@tienda.com").

% Pedidos (Cliente, Producto, Estado, Vendedor, Fecha)
pedido(juan, laptop, pendiente, ana, "2025-03-20").
pedido(juan, mouse, entregado, pedro, "2025-03-15").
pedido(maria, teclado, pendiente, ana, "2025-03-19").
pedido(carlos, monitor, entregado, luis, "2025-03-17").
pedido(juan, smartphone, pendiente, pedro, "2025-03-22").

% Compras anteriores
compra(juan, laptop, 1200, "2024-11-20").
compra(juan, mouse, 25, "2024-12-05").
compra(maria, teclado, 80, "2024-11-12").
compra(carlos, monitor, 250, "2024-10-30").

% Estado de los pedidos
estado_pedido(Cliente, Producto, Estado) :-
    pedido(Cliente, Producto, Estado, _, _).

% Consultar clientes activos o inactivos
clientes_estado(Estado, Lista) :-
    findall(Nombre, cliente(_, Nombre, _, _, Estado), Lista).

% Buscar productos por categoría
productos_categoria(Categoria, Lista) :-
    findall(Nombre, producto(_, Nombre, _, Categoria), Lista).

% Lista de productos comprados por cliente
productos_comprados(Cliente, Lista) :-
    findall((Producto, Precio), compra(Cliente, Producto, Precio, _), Lista).

% Consultar productos pendientes de un cliente
pedidos_pendientes_cliente(Cliente, Lista) :-
    findall(Producto, pedido(Cliente, Producto, pendiente, _, _), Lista).

% Total gastado por cliente en compras
gasto_total_cliente(Cliente, Total) :-
    findall(Precio, compra(Cliente, _, Precio, _), Precios),
    sum_list(Precios, Total).

% Recomendación basada en compras anteriores
recomendar_producto(Cliente, Producto) :-
    compra(Cliente, ProductoComprado, _, _),
    producto(Producto, _, _, _),
    Producto \== ProductoComprado.

% Estado de todos los pedidos de un cliente
estado_pedidos_cliente(Cliente, Lista) :-
    findall((Producto, Estado), pedido(Cliente, Producto, Estado, _, _), Lista).

% Vendedores que han atendido a un cliente
vendedores_cliente(Cliente, Lista) :-
    findall(Vendedor, pedido(Cliente, _, _, Vendedor, _), Lista).
