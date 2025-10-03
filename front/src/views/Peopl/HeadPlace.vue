<template>
  <div data-aos = "fade-down" class="scenic-places">
    <!-- Hero секция -->
    <section class="hero-section">
      <div class="hero-background">
        <div class="gradient-overlay"></div>
        <div class="floating-elements">
          <div class="floating-icon" >
            <i class="pi pi-mountain"></i>
          </div>
        </div>
      </div>
      <div  class="hero-content">
   
            <h1  class="hero-title">
              Живописные места города
              <span class="gradient-text">Орёл</span>
            </h1>
    
        <p  class="hero-subtitle">Откройте для себя удивительную красоту орловских пейзажей</p>
      </div>
    </section>  
  </div>
</template>

<script setup>
</script>

<style scoped>
.scenic-places {
 
  background: var(--bg-secondary);
}

/* Hero Section */
.hero-section {
  position: relative;
  height: 70vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}



.gradient-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(45deg, rgba(102, 126, 234, 0.9), rgba(118, 75, 162, 0.9));
}

.floating-elements {
  position: absolute;
  width: 100%;
  height: 100%;
}

.floating-icon {
  position: absolute;
  font-size: 2rem;
  color: rgba(255, 255, 255, 0.3);
  animation: float 6s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(180deg); }
}

.hero-content {
  position: relative;
  z-index: 2;
  text-align: center;
  color: var(--text-on-gradient);
  max-width: 800px;
  padding: 0 2rem;
}

.hero-title {
  font-size: 4rem;
  font-weight: 700;
  margin-bottom: 1rem;
  line-height: 1.1;
}

.gradient-text {
  background: linear-gradient(45deg, #fff, #f0f4ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.5rem;
  margin-bottom: 3rem;
  opacity: 0.9;
}

.search-bar {
  position: relative;
  max-width: 500px;
  margin: 0 auto;
}

.search-input {
  width: 100%;
  padding: 1.5rem 1.5rem 1.5rem 3.5rem;
  border: none;
  border-radius: var(--radius-lg);
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  font-size: 1.1rem;
  box-shadow: var(--shadow-lg);
  transition: var(--transition-normal);
}

.search-input:focus {
  outline: none;
  box-shadow: var(--shadow-xl);
  transform: translateY(-2px);
}

.search-bar i {
  position: absolute;
  left: 1.5rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
}



.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: var(--bg-primary);
 
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  z-index: var(--z-dropdown);
  margin-top: 0.5rem;
}

.dropdown-item {
  padding: 1rem 1.5rem;
  cursor: pointer;
  transition: var(--transition-fast);
}

.dropdown-item:hover {
  background: var(--bg-secondary);
}

.chip-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.type-chip {
  padding: 0.75rem 1.5rem;
  background: var(--bg-secondary);
  border: 2px solid var(--border-light);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: var(--transition-normal);
  font-weight: 500;
}

.type-chip.active {
  background: var(--primary-gradient);
  color: var(--text-on-gradient);
  border-color: transparent;
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.season-selector {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
}

.season-btn {
  padding: 1rem;
  background: var(--bg-secondary);
 
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: var(--transition-normal);
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.season-btn.active {
  background: var(--accent-gradient);
  color: var(--text-on-gradient);
  border-color: transparent;
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

/* Places Grid */
.places-section {
  padding: 4rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.places-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.place-card {
  background: var(--bg-primary);
  border-radius: var(--radius-xl);
  overflow: hidden;
  box-shadow: var(--shadow-md);
  transition: var(--transition-normal);
  cursor: pointer;
  position: relative;
}

.place-card:hover {
  transform: translateY(-8px);
  box-shadow: var(--shadow-xl);
}

.card-image {
  position: relative;
  height: 250px;
  overflow: hidden;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: var(--transition-slow);
}

.place-card:hover .card-image img {
  transform: scale(1.1);
}

.card-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, transparent, rgba(0, 0, 0, 0.3));
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 1.5rem;
}

.place-badge {
  padding: 0.5rem 1rem;
  border-radius: var(--radius-lg);
  color: var(--text-on-gradient);
  font-weight: 600;
  font-size: 0.875rem;
  backdrop-filter: blur(10px);
}

.favorite-btn {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: var(--transition-normal);
  backdrop-filter: blur(10px);
}

.favorite-btn:hover {
  background: white;
  transform: scale(1.1);
}

.card-content {
  padding: 1.5rem;
}

.place-name {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: var(--text-primary);
}

.place-location {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-secondary);
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.place-description {
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 1.5rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.place-stats {
  display: flex;
  gap: 1.5rem;
}

.stat {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-muted);
  font-size: 0.9rem;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: var(--bg-overlay);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: var(--z-dropdown);
  padding: 2rem;
  backdrop-filter: blur(5px);
}

.modal-content {
  background: var(--bg-primary);
  border-radius: var(--radius-xl);
  max-width: 900px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  box-shadow: var(--shadow-xl);
  animation: modalEnter 0.3s ease-out;
}

@keyframes modalEnter {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.modal-close {
  position: absolute;
  top: 1.5rem;
  right: 1.5rem;
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  background: var(--bg-primary);
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 10;
  box-shadow: var(--shadow-md);
  transition: var(--transition-normal);
}

.modal-close:hover {
  background: var(--bg-secondary);
  transform: rotate(90deg);
}

.modal-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  min-height: 500px;
}

.modal-image {
  position: relative;
  overflow: hidden;
}

.modal-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-badge {
  position: absolute;
  top: 1.5rem;
  left: 1.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: var(--radius-lg);
  color: var(--text-on-gradient);
  font-weight: 600;
  backdrop-filter: blur(10px);
}

.modal-info {
  padding: 3rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.modal-info h2 {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.2;
}

.location-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-secondary);
  font-size: 1.1rem;
}

.modal-description {
  color: var(--text-secondary);
  line-height: 1.7;
  font-size: 1.1rem;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
}

.detail-item i {
  font-size: 1.5rem;
  color: var(--text-muted);
}

.detail-label {
  display: block;
  font-size: 0.875rem;
  color: var(--text-muted);
  margin-bottom: 0.25rem;
}

.detail-value {
  display: block;
  font-weight: 600;
  color: var(--text-primary);
}

.action-buttons {
  display: flex;
  gap: 1rem;
  margin-top: auto;
}

.btn-primary, .btn-secondary {
  flex: 1;
  padding: 1rem 2rem;
  border: none;
  border-radius: var(--radius-lg);
  font-weight: 600;
  cursor: pointer;
  transition: var(--transition-normal);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.btn-primary {
  background: var(--primary-gradient);
  color: var(--text-on-gradient);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.btn-secondary {
  background: var(--bg-secondary);
  color: var(--text-primary);
  border: 2px solid var(--border-light);
}

.btn-secondary.active {
  background: var(--secondary-gradient);
  color: var(--text-on-gradient);
  border-color: transparent;
}

.btn-secondary:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

/* States */
.loading-state, .empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: var(--text-secondary);
}

.loading-spinner {
  width: 3rem;
  height: 3rem;
  border: 3px solid var(--border-light);
  border-top: 3px solid var(--primary-gradient);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1.5rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state i {
  font-size: 4rem;
  margin-bottom: 1.5rem;
  opacity: 0.5;
}

.empty-state h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: var(--text-primary);
}

/* Transitions */
.places-grid-move {
  transition: transform 0.5s ease;
}

.places-grid-enter-active,
.places-grid-leave-active {
  transition: all 0.5s ease;
}

.places-grid-enter-from {
  opacity: 0;
  transform: translateY(30px);
}

.places-grid-leave-to {
  opacity: 0;
  transform: translateY(-30px);
}

.places-grid-leave-active {
  position: absolute;
}

/* Responsive */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }
  
  .hero-subtitle {
    font-size: 1.2rem;
  }
  
  .filters-grid {
    grid-template-columns: 1fr;
  }
  
  .places-grid {
    grid-template-columns: 1fr;
  }
  
  .modal-grid {
    grid-template-columns: 1fr;
  }
  
  .modal-info {
    padding: 2rem;
  }
  
  .action-buttons {
    flex-direction: column;
  }
}

.rotated {
  transform: rotate(180deg);
}
</style>