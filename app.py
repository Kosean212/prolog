from flask import Flask, request, jsonify
from pyswip import Prolog
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permitir solicitudes desde el frontend

prolog = Prolog()

prolog.assertz("cliente(juan, 'Juan Pérez', 'juan@email.com', 5551234, 'activo')")
prolog.assertz("cliente(maria, 'Maria López', 'maria@email.com', 5555678, 'inactivo')")
prolog.assertz("cliente(carlos, 'Carlos Díaz', 'carlos@email.com', 5558765, 'activo')")
prolog.assertz("cliente(ana, 'Ana Gómez', 'ana@email.com', 5554321, 'activo')")
prolog.assertz("producto(laptop, 'Laptop HP', 1200, 'Electrónica')")
prolog.assertz("producto(mouse, 'Mouse Logitech', 25, 'Accesorios')")
prolog.assertz("producto(teclado, 'Teclado Mecánico', 80, 'Accesorios')")
prolog.assertz("producto(monitor, 'Monitor 24 pulgadas', 250, 'Electrónica')")
prolog.assertz("producto(smartphone, 'Smartphone Samsung', 700, 'Electrónica')")
prolog.assertz("producto(cargador, 'Cargador USB-C', 15, 'Accesorios')")
prolog.assertz("pedido(juan, laptop, 'pendiente', 'ana', '2025-03-20')")
prolog.assertz("pedido(juan, mouse, 'entregado', 'pedro', '2025-03-15')")
prolog.assertz("pedido(maria, teclado, 'pendiente', 'ana', '2025-03-19')")
prolog.assertz("pedido(carlos, monitor, 'entregado', 'luis', '2025-03-17')")
prolog.assertz("pedido(juan, smartphone, 'pendiente', 'pedro', '2025-03-22')")
prolog.assertz("compra(juan, laptop, 1200, '2024-11-20')")
prolog.assertz("compra(juan, mouse, 25, '2024-12-05')")
prolog.assertz("compra(maria, teclado, 80, '2024-11-12')")
prolog.assertz("compra(carlos, monitor, 250, '2024-10-30')")

# Ruta para obtener cliente por ID
@app.route('/cliente')
def obtener_cliente():
    cliente_id = request.args.get('id')
    query = f"cliente({cliente_id}, Nombre, Email, Telefono, Estado)"
    resultados = list(prolog.query(query))
    if resultados:
        cliente = resultados[0]
        return jsonify({
            "nombre": cliente["Nombre"],
            "email": cliente["Email"],
            "telefono": cliente["Telefono"],
            "estado": cliente["Estado"]
        })
    return jsonify({"error": "Cliente no encontrado"}), 404

@app.route('/pedidos')
def obtener_pedidos():
    cliente_id = request.args.get('id')
    query = f"pedido({cliente_id}, Producto, Estado, Vendedor, Fecha)"
    pedidos = list(prolog.query(query))
    pedidos_data = [{"producto": pedido["Producto"], "estado": pedido["Estado"]} for pedido in pedidos]
    return jsonify({"pedidos": pedidos_data})

@app.route('/productos')
def obtener_productos():
    categoria = request.args.get('categoria')
    query = f"producto(_, Nombre, _, {categoria})"
    productos = list(prolog.query(query))
    productos_data = [producto["Nombre"] for producto in productos]
    return jsonify({"productos": productos_data})

@app.route('/recomendar')
def recomendar_producto():
    cliente_id = request.args.get('id')
    query_compras = f"compra({cliente_id}, ProductoComprado, _, _)"
    compras = list(prolog.query(query_compras))
    productos_recomendados = []
    for compra in compras:
        query_recom = f"producto(Producto, _, _, _) & Producto \\== {compra['ProductoComprado']}"
        recomendaciones = list(prolog.query(query_recom))
        productos_recomendados.extend([recomendacion["Producto"] for recomendacion in recomendaciones])
    return jsonify({"recomendacion": productos_recomendados or "No hay recomendaciones."})

if __name__ == '__main__':
    app.run(debug=True)
