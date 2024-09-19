<template>
  <div :class="['theme-transition', theme]">
    <!-- Header -->
    <header class="header">
      <div class="logo">
        <img src="https://steamuserimages-a.akamaihd.net/ugc/1654473242722013944/8FECB52BE33AAECD4B8490472012D80243CB262B/?imw=512&amp;imh=495&amp;ima=fit&amp;impolicy=Letterbox&amp;imcolor=%23000000&amp;letterbox=true" alt="Logo" class="logo-image">
      </div>
      <div class="profile-container" @click="toggleMenu">
        <img :src="imgSource" class="profile-image" />
        <span class="username">{{ username }}</span>
      </div>
      <!-- Кнопка переключения темы -->
      <div class="theme-toggle" @click="toggleTheme">
        <img :src="themeIcon" class="theme-icon" />
      </div>
    </header>

    <!-- Sidebar Menu -->
    <div class="dashboard-container">
      <div class="sidebar">
        <div class="profile">
          <div class="profile-pic-container">
            <img :src="imgSource" class="profile-pic" alt="Profile Picture" />
          </div>
        </div>
        <div class="user-id">
          <span>{{ username }}</span>
          <h3>──────────────────────</h3>
          <p>ID: {{ userId }}</p>
          <h3>──────────────────────</h3>
        </div>
        <nav class="menu">
          <ul>
            <li><button @click="$router.push('/')">Главная</button></li>
            <li><button v-if="isLoggedIn" @click="$router.push('/add_product')">Добавить продукт</button></li>
            <li><button v-if="isLoggedIn" @click="$router.push('/check_product')">Просмотр продуктов</button></li>
            <li><button v-if="isLoggedIn" @click="$router.push('/userlist')">Сотрудники</button></li>
            <li><button v-if="isLoggedIn" @click="$router.push('/basket')">Корзина</button></li>
          </ul>
        </nav>
      </div>

      <!-- Main Content -->
      <div class="main-content">
        <router-view></router-view>
      </div>
    </div>

    <!-- Dropdown Menu -->
    <transition name="fade">
      <div v-if="showMenu" class="dropdown-menu">
        <div class="dropdown-header">
          <img :src="imgSource" class="dropdown-profile-image" />
          <div class="dropdown-info">
            <p class="dropdown-username">{{ username }}</p>
            <p class="dropdown-position">{{ position }}</p>
          </div>
        </div>
        <router-link to="/lk" class="menu-link">Личный кабинет</router-link>  
        <button @click="logout" class="logout-button">Выйти из аккаунта</button>
      </div>
    </transition>

    <LoadingSpinner :visible="loading" />
    
    <!-- Modal -->
    <transition name="fade">
      <div v-if="showModal" class="overlay" @click="closeModal"></div>
    </transition>
    <transition name="fade">
      <div v-if="showModal" class="main-popup">
        <div class="popup-header">
          <div id="popup-close-button" @click="closeModal" class="close-button">&times;</div>
          <ul>
            <li :class="{ active: currentForm === 'signIn' }"><a href="#" @click="showForm('signIn')">Войти</a></li>
            <li :class="{ active: currentForm === 'register' }"><a href="#" @click="showForm('register')">Регистрация</a></li>
          </ul>
        </div>
        <div class="popup-content">
          <!-- Форма входа -->
          <form v-if="currentForm === 'signIn'" @submit.prevent="signIn" class="form">
            <label for="username">Никнейм:</label>
            <input type="text" id="username" v-model="signInData.username" placeholder="Имя пользователя" class="input-field" />
            <label for="password">Пароль:</label>
            <input type="password" id="password" v-model="signInData.password" placeholder="Пароль" class="input-field" />
            <p class="check-mark">
              <input type="checkbox" id="remember-me" v-model="signInData.rememberMe" class="checkbox" />
              <label for="remember-me">Запомнить меня</label>
            </p>
            <input type="submit" id="submit" value="Войти" class="submit-button" />
          </form>

          <!-- Форма регистрации -->
          <form v-if="currentForm === 'register'" @submit.prevent="register" class="form">
            <label for="username-register">Никнейм:</label>
            <input type="text" id="username-register" v-model="registerData.username" placeholder="Имя пользователя" class="input-field" />
            <label for="email-register">Электронная почта:</label>
            <input type="email" id="email-register" v-model="registerData.email" placeholder="Email" class="input-field" />
            <label for="password-register">Пароль:</label>
            <input type="password" id="password-register" v-model="registerData.password" placeholder="Пароль" class="input-field" />
            <label for="password-confirmation">Подтвердите пароль:</label>
            <input type="password" id="password-confirmation" v-model="registerData.passwordConfirmation" placeholder="Подтвердите пароль" class="input-field" />
            <p class="check-mark">
              <input type="checkbox" id="accept-terms" v-model="registerData.acceptTerms" class="checkbox" />
              <label for="accept-terms">Я согласен с <a href="#">условиями</a></label>
            </p>
            <input type="submit" id="submit" value="Создать аккаунт" class="submit-button" />
          </form>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'App',
  data() {
    return {
      showMenu: false,
      showModal: false,
      currentForm: 'signIn',
      signInData: {
        username: '',
        password: '',
        rememberMe: false
      },
      registerData: {
        username: '',
        email: '',
        password: '',
        passwordConfirmation: '',
        acceptTerms: false
      },
      username: '',
      position: '',
      imgSource: 'https://via.placeholder.com/50',
      userId: null,  // Added userId to store the user's ID
      theme: 'theme-light', // Добавлена переменная для темы
      themeIcon: 'path/to/light-theme-icon.png', // Иконка для светлой темы
    };
  },
  computed: {
  isLoggedIn() {
    return !!localStorage.getItem('access_token') || localStorage.getItem('guest') === 'true';
  },
},
  methods: {
    toggleMenu() {
      this.showMenu = !this.showMenu;
    },
    logout() {
      localStorage.removeItem('access_token');
  localStorage.removeItem('guest');

  // Сбрасываем данные пользователя
  this.username = '';
  this.position = '';
  this.imgSource = 'https://via.placeholder.com/50';
  this.userId = null;

  // Скрываем меню, если оно открыто
  this.showMenu = false;

  // Перенаправляем на страницу HomePage
  this.$router.push('/');
  
},
    openModal() {
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
    },
    showForm(formType) {
      this.currentForm = formType;
    },
    async signIn() {
      try {
        const response = await axios.post('http://localhost:8000/users/login', {
          username: this.signInData.username,
          password: this.signInData.password,
        });
        localStorage.setItem('access_token', response.data.access_token);
        this.closeModal();
        window.location.reload(); // Обновление страницы после входа
        this.loadUserProfile();
      } catch (error) {
        console.error('Ошибка входа:', error);
        alert('Ошибка входа. Проверьте введенные данные.');
      }
    },
    async register() {
      try {
        if (this.registerData.password !== this.registerData.passwordConfirmation) {
          alert('Пароли не совпадают');
          return;
        }
        if (!this.registerData.acceptTerms) {
          alert('Необходимо согласие с условиями');
          return;
        }
        await axios.post('http://localhost:8000/users/register', {
          username: this.registerData.username,
          email: this.registerData.email,
          password: this.registerData.password,
        });
        alert('Регистрация успешна. Теперь вы можете войти.');
        this.showForm('signIn');
      } catch (error) {
        console.error('Ошибка регистрации:', error);
        alert('Ошибка регистрации. Пожалуйста, попробуйте еще раз.');
      }
    },
    async loadUserProfile() {
      if (this.isLoggedIn) {
        try {
          const token = localStorage.getItem('access_token');
          const response = await axios.get('http://localhost:8000/employees/user-employee/', {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });

          const user = response.data;
          this.username = user.FIO;
          this.position = user.post;
          this.userId = user.id; // Set userId
          this.loadUserPhoto(user.id);
        } catch (error) {
          console.error('Ошибка при загрузке данных пользователя:', error);
        }
      }
    },
    async loadUserPhoto(userId) {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get(`http://localhost:8000/employees/${userId}/photo/`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
          responseType: 'blob',
        });

        if (response.data) {
          this.imgSource = URL.createObjectURL(response.data);
        }
      } catch (error) {
        console.error('Ошибка при загрузке фото пользователя:', error);
      }
    },
    toggleTheme() {
      if (this.theme === 'theme-light') {
        this.theme = 'theme-dark';
        this.themeIcon = 'path/to/dark-theme-icon.png'; // Иконка для тёмной темы
      } else {
        this.theme = 'theme-light';
        this.themeIcon = 'path/to/light-theme-icon.png'; // Иконка для светлой темы
      }
    }
  },
  mounted() {
    this.loadUserProfile();
  },
};
</script>


<style scoped>
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  font-family: 'Arial', sans-serif;
}

/* Основные стили */
#app {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
}

/* Шапка */
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px 30px;
  width: 100%;
  box-sizing: border-box;
  position: fixed;
  top: 0;
  z-index: 1000;
  transition: background-color 0.5s ease, color 0.5s ease;
}

/* Боковое меню */
.sidebar {
  position: fixed;
  top: 70px;
  left: 0;
  width: 250px;
  height: calc(100% - 70px);
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow-y: auto;
  transition: background-color 0.5s ease;
}

/* Основной контент */
.main-content {
  margin-left: 250px;
  padding: 20px;
  width: calc(100% - 250px);
  transition: background-color 0.5s ease;
}

/* Смена темы */
.theme-light .header {
  background-color: #d3d3d3; /* Светло-серый цвет для шапки */
  color: #333;
}

.theme-light .sidebar {
  background-color: #e5e5e5; /* Еще светлее серый цвет для бокового меню */
}

.theme-light .main-content {
  background-color: #ffffff; /* Белый цвет фона для основного контента */
}

.theme-dark .header {
  background-color: #333; /* Темный цвет для шапки */
  color: #eaeaea;
}

.theme-dark .sidebar {
  background-color: #444; /* Темный цвет для бокового меню */
}

.theme-dark .main-content {
  background-color: #2f2f2f; /* Темно-синий фон для основного контента */
}

/* Прочие стили (сохранены как есть) */
.logo-image {
  height: 50px;
}

.profile-container {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.profile-image {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 10px;
}

.username {
  font-weight: bold;
  font-family: 'Arial', sans-serif;
}

/* Боковое меню */
.sidebar.theme-light {
  background-color: #e0e0e0; /* Светлее серый для светлой темы */
}

.sidebar.theme-dark {
  background-color: #2e2e2e; /* Тёмный для тёмной темы */
}

.menu ul li button {
  color: #333; /* Цвет шрифта по умолчанию */
}

.theme-light .menu ul li button {
  color: #333; /* Цвет шрифта для светлой темы */
}

.theme-dark .menu ul li button {
  color: #eaeaea; /* Цвет шрифта для тёмной темы */
}

.menu ul li button:hover {
  background-color: rgb(246, 164, 0); /* Оставляем этот цвет для подсветки при наведении */
  color: white; /* Цвет текста при наведении */
}

.profile-pic-container {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  overflow: hidden;
  margin-bottom: 10px;
}

.profile-pic {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-id {
  font-family: 'Arial', serif;
  color: #f1f1f1;
  margin-bottom: 20px;
  text-align: center;
}

.user-id span {
  color: #f1f1f1; /* Цвет текста ID и имени для светлой темы */
}

/* Светлая тема */
.theme-light .user-id span {
  color: #333; /* Цвет для имени пользователя и ID в светлой теме */
}

/* Темная тема */
.theme-dark .user-id span {
  color: #eaeaea; /* Цвет для имени пользователя и ID в темной теме */
}

/* Светлая тема */
.theme-light .header {
  background-color: #d3d3d3;
  color: #333;
}

.theme-light .sidebar {
  background-color: #e5e5e5;
}

.theme-light .main-content {
  background-color: #ffffff;
}

.theme-light .user-id {
  color: #333;
}

.theme-light .user-id span {
  color: #333;
}

/* Темная тема */
.theme-dark .header {
  background-color: #333;
  color: #eaeaea;
}

.theme-dark .sidebar {
  background-color: #444;
}

.theme-dark .main-content {
  background-color: #2f2f2f;
}

.theme-dark .user-id {
  color: #eaeaea;
}

.theme-dark .user-id span {
  color: #eaeaea;
}


.theme-dark .user-id {
  color: #eaeaea; /* Цвет текста ID и имени для темной темы */
}

.theme-dark .user-id span {
  color: #eaeaea; /* Цвет текста ID для темной темы */
}

.menu ul {
  list-style-type: none;
  padding: 0;
}

.menu ul li {
  margin: 15px 0;
}

.menu ul li button {
  background: none;
  border: none;
  color: #ddd;
  cursor: pointer;
  text-align: left;
  font-size: 16px;
  width: 100%;
  padding: 10px;
  border-radius: 5px;
}

.menu ul li button:hover {
  background-color: rgb(246, 164, 0);
  color: white;
}

/* Dropdown Menu */
.dropdown-menu {
  position: fixed;
  top: 84px;
  right: 620px;
  background: rgb(246, 164, 0);
  color: rgb(255, 255, 255);
  font-family: 'Arial', sans-serif;
  border-radius: 8px;
  z-index: 1000;
  width: 250px;
}
.theme-light .dropdown-header{
  background: #d3d3d3;
}
.theme-dark .dropdown-header{
  background: #333;
}

/* Light theme for dropdown menu text */
.theme-light .dropdown-menu {
  background-color: #d3d3d3; /* already present */
  color: #333; /* Dark text for light theme */
}

.theme-light .dropdown-info {
  color: #333; /* Ensure dropdown user info text is dark */
}

.theme-light .menu-link {
  color: #333; /* Dark text for links in the dropdown */
}

.theme-light .logout-button {
  color: #fff; /* White text for the logout button */
}

/* Dark theme for dropdown menu text */
.theme-dark .dropdown-menu {
  background-color: #333; /* already present */
  color: #eaeaea; /* Light text for dark theme */
}

.theme-dark .dropdown-info {
  color: #eaeaea; /* Light text for user info in dropdown */
}

.theme-dark .menu-link {
  color: #eaeaea; /* Light text for links in the dropdown */
}

.theme-dark .logout-button {
  color: #fff; /* White text for the logout button */
}


.dropdown-header {
  display: flex;
  align-items: center;
  padding: 15px;
  background-color: rgb(243, 233, 57);
}

.dropdown-profile-image {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
}

.dropdown-info {
  flex-grow: 1;
}

.dropdown-username {
  font-weight: bold;
  margin: 0;
}

.dropdown-position {
  font-size: 0.9em;
  color:rgb(246,164,0);
  font-family: 'Arial', sans-serif;
  margin: 0;
}

.menu-link {
  display: block;
  padding: 15px;
  color: rgb(255, 255, 255);
  font-family: 'Arial', sans-serif;
  text-decoration: none;
  transition: background-color 0.3s;
}

.menu-link:hover {
  background-color: rgb(246,164,0);
}

.logout-button {
  display: block;
  width: 100%;
  color: rgb(255, 255, 255);
  background-color: red;
  border: none;
  padding: 15px;
  cursor: pointer;
  text-align: left;
  transition: background-color 0.3s;  
}

.logout-button:hover {
  font-family: 'Arial', sans-serif;
  background-color: rgb(246,164,0);
}

/* Modal Styles */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 999;
}

.main-popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  width: 300px;
}

.popup-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.popup-header ul {
  display: flex;
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.popup-header li {
  margin-right: 20px;
}

.popup-header a {
  text-decoration: none;
  color: black;
  font-weight: bold;
}

.popup-header li.active a {
  color: #fd6a02;
}

.popup-content {
  padding-top: 10px;
}

.form label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form .input-field {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.form .checkbox {
  margin-right: 5px;
}

.form .submit-button {
  width: 100%;
  padding: 10px;
  background-color: #fd6a02;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1em;
}

.form .submit-button:hover {
  background-color: #e05a02;
}

.close-button {
  font-size: 20px;
  cursor: pointer;
}

/* Transition Animations */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* одно и то же, что и fade-leave-active в версии ниже 2.1.8 */ {
  opacity: 0;
}

.theme-toggle-button {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: #ff9800;
  border: none;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  z-index: 1000;
}

.theme-toggle-button img {
  width: 24px;
  height: 24px;
}

</style>
