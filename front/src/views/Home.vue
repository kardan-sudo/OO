<script setup></script>

<template>
  <div data-aos="fade-left" class="hero-section">
    <img src="../assets/1.jpg" alt="Орёл — город гениев слова" />
    <div class="hero-overlay"></div>
    <div class="hero-content">
      <h1 class="hero-title">Орёл: город вдохновения</h1>
      <p class="hero-subtitle">
        Город, подаривший миру гениев слова. Откройте места, где рождались бессмертные произведения, и почувствуйте творческую энергию, что до сих пор витает в орловском воздухе.
      </p>
    </div>
  </div>
</template>

<style scoped>
.hero-section {
  position: relative;
  height: calc(100vh - 80px);
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  margin-top: 80px;
}

.hero-section img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: 1;
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5); /* немного затемнено для контраста */
  z-index: 2;
}

.hero-content {
  position: relative;
  z-index: 3;
  max-width: 850px;
  padding: 0 1.5rem;
  text-align: center;
  color: white;
}

/* Главный заголовок */
.hero-title {
  font-size: 3.2rem;
  font-weight: 800;
  line-height: 1.2;
  margin: 0 0 1.2rem;
  text-shadow: 0 4px 12px rgba(0, 0, 0, 0.6);
  background: linear-gradient(to right, #ffd700, #ffffff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.5px;
}

/* Подзаголовок */
.hero-subtitle {
  font-size: 1.4rem;
  font-weight: 400;
  line-height: 1.5;
  margin: 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
  opacity: 0.95;
}

/* Адаптивность */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.2rem;
    margin-bottom: 1rem;
  }

  .hero-subtitle {
    font-size: 1.15rem;
    padding: 0 0.8rem;
  }

  .hero-section {
    height: calc(100vh - 70px);
    margin-top: 70px;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 1.8rem;
    line-height: 1.25;
  }

  .hero-subtitle {
    font-size: 1rem;
    line-height: 1.5;
    padding: 0 0.6rem;
  }
}
</style>