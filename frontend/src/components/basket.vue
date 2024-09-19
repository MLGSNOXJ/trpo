<template>
  <div class="cart-container">
    <div class="cart-content">
      <h1>Корзина</h1>
      <div v-if="cartItems.length === 0" class="empty-cart">
        Ваша корзина пуста.
      </div>
      <div v-else>
        <ul class="cart-list">
          <li v-for="item in cartItems" :key="item.id" class="cart-item">
            <!-- Display product image -->
            <div class="item-image">
              <img :src="item.image || '/images/default-image.jpg'" :alt="item.name" />
            </div>
            <div class="item-details">
              <h3>{{ item.name }}</h3>
              <p>{{ item.description }}</p>
              <div class="item-quantity">
                <button @click="decreaseQuantity(item)" class="quantity-btn">-</button>
                <span>{{ item.quantity }}</span>
                <button @click="increaseQuantity(item)" class="quantity-btn">+</button>
              </div>
              <div class="item-price">
                <span>{{ item.cost * item.quantity }} руб.</span>
              </div>
              <button @click="removeItem(item.id)" class="remove-btn">Удалить</button>
            </div>
          </li>
        </ul>
      </div>
    </div>
    <div class="cart-summary">
      <p>Ваша корзина</p>
      <p>Товары ({{ totalItems }})</p>
      <p>Итого: {{ totalPrice }} руб.</p>
      <button class="checkout-btn">Перейти к оформлению</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      cartItems: [],
    };
  },
  computed: {
    totalPrice() {
      return this.cartItems.reduce((total, item) => total + item.cost * item.quantity, 0);
    },
    totalItems() {
      return this.cartItems.reduce((total, item) => total + item.quantity, 0);
    },
  },
  methods: {
    async fetchImageForProduct(productId) {
      try {
        const response = await axios.get(`http://localhost:8000/products/products/${productId}/photo`, {
          responseType: 'blob',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          }
        });
        return URL.createObjectURL(response.data);
      } catch (error) {
        console.error('Ошибка при загрузке фото', error);
        return '/images/default-image.jpg';
      }
    },
    async loadCartItems() {
      const savedCart = JSON.parse(localStorage.getItem('cart')) || [];
      // Fetch images for all cart items
      for (let item of savedCart) {
        item.image = await this.fetchImageForProduct(item.id);
      }
      this.cartItems = savedCart.map(item => ({
        ...item,
        quantity: item.quantity || 1, // Default quantity to 1 if not set
      }));
    },
    increaseQuantity(item) {
      item.quantity++;
    },
    decreaseQuantity(item) {
      if (item.quantity > 1) {
        item.quantity--;
      }
    },
    removeItem(id) {
      this.cartItems = this.cartItems.filter(item => item.id !== id);
    },
  },
  async created() {
    await this.loadCartItems();
  },
  watch: {
    cartItems: {
      handler(newVal) {
        localStorage.setItem('cart', JSON.stringify(newVal));
      },
      deep: true,
    },
  },
};
</script>

<style scoped>
.cart-container {
  display: flex;
  flex-direction: column;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  font-family: 'Roboto', sans-serif;
}

.cart-content {
  flex: 1;
  margin-bottom: 20px;
}

.cart-summary {
  flex: 1;
  padding: 40px;
  background-color: #f9f9f9;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

h1 {
  font-size: 26px;
  margin-bottom: 20px;
  color: #f6a400;
  font-weight: 700;
}

.empty-cart {
  text-align: center;
  padding: 40px;
  font-size: 18px;
  color: #777;
}

.cart-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.cart-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px;
  background-color: #fff;
  margin-bottom: 10px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.item-image img {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 8px;
}

.item-details {
  flex: 1;
  margin-left: 20px;
}

.item-details h3 {
  margin: 0;
  font-size: 20px;
  color: #333;
  font-weight: 600;
}

.item-details p {
  margin: 5px 0 10px;
  font-size: 14px;
  color: #555;
}

.item-quantity {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.quantity-btn {
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  padding: 5px 10px;
  cursor: pointer;
  font-size: 16px;
  border-radius: 4px;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.quantity-btn:hover {
  background-color: #e0e0e0;
}

.item-price {
  font-size: 16px;
  color: #333;
  font-weight: bold;
}

.remove-btn {
  background-color: #ff4d4d;
  color: #fff;
  border: none;
  padding: 6px 12px;
  cursor: pointer;
  font-size: 14px;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

.remove-btn:hover {
  background-color: #e60000;
}

.cart-summary p {
  font-size: 16px;
  margin-bottom: 10px;
  color: #333;
}

.checkout-btn {
  background-color: #2ecc71;
  color: #fff;
  border: none;
  padding: 12px 20px;
  cursor: pointer;
  font-size: 16px;
  margin-top: 20px;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

.checkout-btn:hover {
  background-color: #27ae60;
}

@media (min-width: 768px) {
  .cart-container {
    flex-direction: row;
  }

  .cart-content {
    flex: 3;
    margin-right: 20px;
  }

  .cart-summary {
    flex: 1;
  }
}
</style>
