<template>
  <div class="product-page">
    <h1 class="page-title">Список продуктов</h1>
    
    <!-- Products Table -->
    <div class="table-container">
      <table class="product-table">
        <thead>
          <tr>
            <th>Фото</th> <!-- New column for photo -->
            <th @click="sortBy('name')">Название <span :class="getSortClass('name')"></span></th>
            <th @click="sortBy('manufacturer')">Производитель <span :class="getSortClass('manufacturer')"></span></th>
            <th @click="sortBy('article_p')">Артикул (п) <span :class="getSortClass('article_p')"></span></th>
            <th @click="sortBy('article_v')">Артикул (в) <span :class="getSortClass('article_v')"></span></th>
            <th @click="sortBy('cost')">Цена <span :class="getSortClass('cost')"></span></th>
            <th @click="sortBy('factory_number')">Заводской номер <span :class="getSortClass('factory_number')"></span></th>
            <th @click="sortBy('storage_location.shelving_number')">Стеллаж <span :class="getSortClass('storage_location.shelving_number')"></span></th>
            <th @click="sortBy('storage_location.shelf_number')">Полка <span :class="getSortClass('storage_location.shelf_number')"></span></th>
            <th>Количество</th> <!-- New column for quantity -->
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in paginatedProducts" :key="product.id">
            <td class="product-photo-column"
                @mouseover="showPhotoPopup($event, product)"
                @mousemove="updatePopupPosition($event)"
                @mouseleave="hidePhotoPopup">
              <img :src="product.photoUrl || '/images/default-image.jpg'" alt="Фото" class="product-photo" />
            </td>
            <td class="product-name-column">
              {{ product.name }}
            </td>
            <td>{{ product.manufacturer }}</td>
            <td>{{ product.article_p }}</td>
            <td>{{ product.article_v }}</td>
            <td>{{ product.cost }} руб.</td>
            <td>{{ product.factory_number }}</td>
            <td>{{ product.storage_location.shelving_number }}</td>
            <td>{{ product.storage_location.shelf_number }}</td>
            <td>{{ product.quantity }}</td> <!-- Display the product quantity -->
            <td>
              <button @click="addToCart(product)">Добавить в корзину</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Всплывающее окно с увеличенным фото -->
    <div v-if="showPopup"
                :style="{ top: popupPosition.y + 'px', left: popupPosition.x + 'px' }"
                class="photo-popup">
              <img :src="popupImageUrl" alt="Фото" />
            </div>
    <!-- Pagination Controls -->
    <div class="pagination-controls">
      <button @click="prevPage" :disabled="currentPage === 1">Предыдущая</button>
      <span>Страница {{ currentPage }} из {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage === totalPages">Следующая</button>
    </div>

    <!-- Filters Block -->
    <div class="filters-container">
      <!-- Warehouse Filter -->
      <div class="filter warehouse-filter">
        <label for="warehouse-select" class="filter-label">Выберите склад:</label>
        <select id="warehouse-select" v-model="selectedWarehouse" @change="filterByWarehouse" class="filter-select">
          <option :value="null">Все склады</option>
          <option v-for="warehouse in warehouses" :key="warehouse.id" :value="warehouse">
            {{ warehouse.name }}
          </option>
        </select>
      </div>

      <!-- Employee Filter -->
      <div class="filter employee-filter">
        <label for="employee-select" class="filter-label">Выберите сотрудника:</label>
        <select id="employee-select" v-model="selectedEmployee" @change="filterByEmployee" class="filter-select">
          <option :value="null">Все сотрудники</option>
          <option v-for="employee in employees" :key="employee.id" :value="employee">
            {{ employee.FIO }}
          </option>
        </select>
      </div>

      <!-- Product Search -->
      <div class="filter product-search">
        <label for="product-search-input" class="filter-label">Поиск по названию:</label>
        <input 
          id="product-search-input" 
          v-model="searchQuery" 
          type="text" 
          placeholder="Введите название продукта" 
          @input="resetPagination" 
          class="search-input"
        />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ProductPage',
  data() {
    return {
      products: [],
      employees: [],
      warehouses: [],
      selectedWarehouse: null,
      selectedEmployee: null,
      searchQuery: '',
      sortKey: 'name',
      sortOrder: 'asc',
      currentPage: 1, // Current page number
      pageSize: 2,   // Number of products per page
      showPopup: false, 
      popupImageUrl: '', 
      popupPosition: { x: 0, y: 0 } 
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.filteredProducts().length / this.pageSize);
    },
    paginatedProducts() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.sortedProducts().slice(start, end);
    },
    isLoggedIn() {
      return !!localStorage.getItem('access_token');
    }
  },
  methods: {
    async fetchProducts() {
      try {
        const response = await axios.get('http://localhost:8000/products/', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          }
        });
        if (response.status === 200) {
          this.products = response.data.map(product => ({
          ...product,
          photoUrl: `http://localhost:8000/products/products/${product.id}/photo`
        }));
        } else {
          console.error('Ошибка при получении списка продуктов');
        }
      } catch (error) {
        console.error('Ошибка при подключении к серверу', error);
      }
    },
    async fetchEmployees() {
      try {
        const response = await axios.get('http://localhost:8000/employees/', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          }
        });
        if (response.status === 200) {
          this.employees = response.data;
        } else {
          console.error('Ошибка при получении списка сотрудников');
        }
      } catch (error) {
        console.error('Ошибка при подключении к серверу', error);
      }
    },
    async fetchWarehouses() {
      try {
        const response = await axios.get('http://localhost:8000/products/warehouses/', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          }
        });
        if (response.status === 200) {
          this.warehouses = response.data;
        } else {
          console.error('Ошибка при получении списка складов');
        }
      } catch (error) {
        console.error('Ошибка при подключении к серверу', error);
      }
    },
    filterByWarehouse() {
      this.resetPagination();
    },
    filterByEmployee() {
      this.resetPagination();
    },
    sortBy(key) {
      if (this.sortKey === key) {
        this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
      } else {
        this.sortKey = key;
        this.sortOrder = 'asc';
      }
      this.resetPagination();
    },
    getSortClass(column) {
      if (this.sortKey !== column) return '';
      return this.sortOrder === 'asc' ? 'sort-asc' : 'sort-desc';
    },
    filteredProducts() {
      let products = this.products;

      if (this.selectedWarehouse) {
        products = products.filter(product => product.warehouse_id === this.selectedWarehouse.id);
      }

      if (this.selectedEmployee) {
        products = products.filter(product => product.employee_id === this.selectedEmployee.id);
      }

      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        products = products.filter(product => product.name.toLowerCase().includes(query));
      }

      return products;
    },
    sortedProducts() {
      return this.filteredProducts().sort((a, b) => {
        let comparison = 0;
        if (a[this.sortKey] > b[this.sortKey]) {
          comparison = 1;
        } else if (a[this.sortKey] < b[this.sortKey]) {
          comparison = -1;
        }
        return this.sortOrder === 'asc' ? comparison : -comparison;
      });
    },
    addToCart(product) {
      let cart = JSON.parse(localStorage.getItem('cart')) || [];
      
      const index = cart.findIndex(item => item.id === product.id);
      if (index === -1) {
        cart.push(product);
        localStorage.setItem('cart', JSON.stringify(cart));
        alert('Продукт добавлен в корзину');
      } else {
        alert('Продукт уже в корзине');
      }
    },
    showPhotoPopup(event, product) {
    this.popupImageUrl = product.photoUrl || '/images/default-image.jpg';
    this.popupPosition = { x: event.clientX + 20, y: event.clientY + 20 };
    this.showPopup = true;
     }, 
     updatePopupPosition(event) {
    this.popupPosition = { x: event.clientX + 20, y: event.clientY + 20 };
    },
    hidePhotoPopup() {
    this.showPopup = false;
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage += 1;
      }
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage -= 1;
      }
    },
    resetPagination() {
      this.currentPage = 1;
    }
  },
  mounted() {
    this.fetchProducts();
    this.fetchEmployees();
    this.fetchWarehouses();
  }
};
</script>

<style scoped>
/* Стили для 100% высоты страницы */
html, body {
  height: 100%;
  margin: 0;
  padding: 0;
  background-color: #2e2e2e; /* Убедитесь, что фон соответствует теме */
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh; /* 100% высоты окна */
  background-color: #2e2e2e; /* Задаем фон */
}

main {
  flex: 1; /* Основной контент займет оставшуюся высоту */
  padding: 20px; /* Отступы для содержимого */
  background-color: #2e2e2e;
}

.product-page {
  font-family: 'Arial', sans-serif;
  min-height: 100vh; /* Минимальная высота, чтобы занимать всю высоту страницы */
  display: flex;
  flex-direction: column;
  padding: 60px 20px 20px 20px; /* Отступ сверху для отступа от шапки */
  box-sizing: border-box; /* Включаем padding в расчеты высоты */
}

.page-title {
  font-size: 2rem;
  text-align: center;
  margin-bottom: 20px;
  font-weight: bold;
}

.theme-light .page-title {
  color: #333; /* Темный текст в светлой теме */
}

.theme-dark .page-title {
  color: #fff; /* Белый текст в темной теме */
}

.filters-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

.filter {
  padding: 10px;
  border-radius: 4px; /* Угловатые элементы */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 250px; /* Сужаем ширину фильтров */
}

.theme-light .filter {
  background: #f4f4f4;
  color: #333; /* Цвет текста в светлой теме */
}

.theme-dark .filter {
  background: #333;
  color: #eaeaea; /* Цвет текста в темной теме */
}

.filter-label {
  display: block;
  margin-bottom: 5px;
  font-weight: 600;
}

.filter-select,
.search-input {
  width: 100%;
  padding: 8px; /* Уменьшаем padding для более угловатого вида */
  border-radius: 4px; /* Угловатые элементы */
  font-size: 0.9rem; /* Уменьшаем размер шрифта */
  border: 2px solid transparent;
  background: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: border-color 0.3s, box-shadow 0.3s;
}

.theme-light .filter-select,
.theme-light .search-input {
  border-color: #ccc;
  color: #333;
}

.theme-dark .filter-select,
.theme-dark .search-input {
  background: #444;
  border-color: #555;
  color: #eaeaea;
}

.filter-select:focus,
.search-input:focus {
  border-color: #888;
  box-shadow: 0 0 4px rgba(0, 0, 0, 0.2);
  outline: none;
}

.table-container {
  margin: 20px auto 40px auto; /* Добавлен нижний отступ для разделения таблицы и фильтров */
  max-width: 90%; /* Сужаем таблицу */
  overflow-x: auto; /* Добавляем прокрутку по горизонтали при необходимости */
}

.product-table {
  width: 100%;
  border-collapse: collapse;
  border-radius: 4px; /* Угловатые элементы */
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Уменьшаем тень */
}

.theme-light .product-table {
  background: #fff;
  color: #333;
}

.theme-dark .product-table {
  background: #2e2e2e;
  color: #eaeaea;
}

.product-table th,
.product-table td {
  border: 1px solid #ddd;
  padding: 10px 15px; /* Уменьшаем padding для более угловатого вида */
  text-align: left;
  font-size: 0.9rem; /* Уменьшаем размер шрифта */
}

.theme-light .product-table th {
  background: #555;
  color: #fff;
}

.theme-dark .product-table th {
  background: #444;
  color: #eaeaea;
}

.product-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.theme-dark .product-table tr:nth-child(even) {
  background-color: #3e3e3e;
}

.product-table tr:hover {
  background-color: #d3d3d3;
}

.theme-dark .product-table tr:hover {
  background-color: #5e5e5e;
}

.product-photo {
  width: 60px; /* Уменьшаем размер фото */
  height: 60px;
  object-fit: cover;
  border-radius: 4px;
}

.photo-popup {
  position: absolute;
  z-index: 1000;
  border: 2px solid #888;
  background-color: #fff;
  padding: 10px;
  border-radius: 4px; /* Угловатые элементы */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Уменьшаем тень */
}

.theme-dark .photo-popup {
  background-color: #444;
  border-color: #555;
  color: #eaeaea;
}

.photo-popup img {
  max-width: 180px; /* Уменьшаем максимальный размер фото в попапе */
  max-height: 180px;
  border-radius: 4px; /* Угловатые элементы */
}

.pagination-controls {
  text-align: center;
  margin: 20px 0;
}

.pagination-controls button {
  background-color: #4CAF50; /* Цвет кнопок */
  color: white;
  border: none;
  padding: 10px 20px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
  border-radius: 4px; /* Угловатые элементы */
}

.pagination-controls button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

</style>
