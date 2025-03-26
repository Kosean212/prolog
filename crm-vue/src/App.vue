<template>
  <div class="container">
    <h1>CRM - Gestión de Clientes</h1>

    <div class="card">
      <input v-model="clienteID" placeholder="Ingrese ID del cliente" />
      <button @click="obtenerCliente">Buscar Cliente</button>
      <button @click="obtenerPedidos">Ver Pedidos</button>
      <button @click="recomendarProducto">Recomendar Producto</button>
    </div>

    <div v-if="cliente" class="card">
      <h2>Datos del Cliente</h2>
      <p><strong>Nombre:</strong> {{ cliente.nombre }}</p>
      <p><strong>Email:</strong> {{ cliente.email }}</p>
      <p><strong>Teléfono:</strong> {{ cliente.telefono }}</p>
      <p><strong>Estado:</strong> {{ cliente.estado }}</p>
    </div>

    <div v-if="pedidos.length" class="card">
      <h2>Pedidos</h2>
      <ul>
        <li v-for="pedido in pedidos" :key="pedido.producto">{{ pedido.producto }} - {{ pedido.estado }}</li>
      </ul>
    </div>

    <div v-if="recomendacion" class="card">
      <h2>Producto Recomendado</h2>
      <ul>
        <li v-for="producto in recomendacion" :key="producto">{{ producto }}</li>
      </ul>
    </div>

    <div class="card">
      <input v-model="categoria" placeholder="Ingrese categoría" />
      <button @click="obtenerProductos">Buscar Productos</button>
    </div>

    <div v-if="productos.length" class="card">
      <h2>Productos</h2>
      <ul>
        <li v-for="producto in productos" :key="producto">{{ producto }}</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const clienteID = ref('');
const cliente = ref(null);
const pedidos = ref([]);
const productos = ref([]);
const categoria = ref('');
const recomendacion = ref([]);

const obtenerCliente = async () => {
  if (!clienteID.value) return;
  try {
    const res = await axios.get(`http://127.0.0.1:5000/cliente?id=${clienteID.value}`);
    cliente.value = res.data;
  } catch (error) {
    cliente.value = null;
    alert('Cliente no encontrado.');
  }
};

const obtenerPedidos = async () => {
  if (!clienteID.value) return;
  try {
    const res = await axios.get(`http://127.0.0.1:5000/pedidos?id=${clienteID.value}`);
    pedidos.value = res.data.pedidos;
  } catch (error) {
    pedidos.value = [];
    alert('No se encontraron pedidos.');
  }
};

const obtenerProductos = async () => {
  if (!categoria.value) return;
  try {
    const res = await axios.get(`http://127.0.0.1:5000/productos?categoria=${categoria.value}`);
    productos.value = res.data.productos;
  } catch (error) {
    productos.value = [];
    alert('No se encontraron productos.');
  }
};

const recomendarProducto = async () => {
  if (!clienteID.value) return;
  try {
    const res = await axios.get(`http://127.0.0.1:5000/recomendar?id=${clienteID.value}`);
    recomendacion.value = res.data.recomendacion;
  } catch (error) {
    recomendacion.value = [];
    alert('No hay recomendaciones.');
  }
};
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: auto;
  text-align: center;
  color: #111010;
  font-family: Arial, sans-serif;
}
.card {
  background: #f4f4f4;
  padding: 15px;
  margin: 15px 0;
  border-radius: 8px;
}
input {
  padding: 8px;
  margin-right: 10px;
  border-radius: 4px;
  border: 1px solid #111010;
}
button {
  padding: 8px 15px;
  border: none;
  border-radius: 4px;
  background: #007bff;
  color: rgb(24, 22, 22);
  cursor: pointer;
}
button:hover {
  background: #0056b3;
}
</style>
