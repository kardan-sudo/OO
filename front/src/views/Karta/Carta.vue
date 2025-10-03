<template>
    <div ref="map" style="width: 100%; height: 400px;"></div>
  </template>
  
  <script>
  export default {
    name: 'LeafletMap',
    mounted() {
      
      if (!window.L) {
        const link = document.createElement('link')
        link.rel = 'stylesheet'
        link.href = 'https://unpkg.com/leaflet@1.7.1/dist/leaflet.css'
        document.head.appendChild(link)
  
        const script = document.createElement('script')
        script.src = 'https://unpkg.com/leaflet@1.7.1/dist/leaflet.js'
        script.onload = this.initMap
        document.head.appendChild(script)
      } else {
        this.initMap()
      }
    },
    methods: {
      initMap() {
        // Координаты центра Орла
        const map = L.map(this.$refs.map).setView([52.9685, 36.0693], 13)
  
        // Добавляем тайлы OpenStreetMap
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          attribution: '© OpenStreetMap'
        }).addTo(map)
  
        // Добавляем основные точки Орла
        const points = [
          { 
            lat: 52.9685, 
            lng: 36.0693, 
            title: "Центр Орла",
            description: "Площадь Ленина, центр города"
          },
          { 
            lat: 52.9714, 
            lng: 36.0647, 
            title: "Орловский краеведческий музей",
            description: "ул. Гостиная, 2"
          },
          { 
            lat: 52.9667, 
            lng: 36.0789, 
            title: "Железнодорожный вокзал",
            description: "Привокзальная площадь"
          },
          { 
            lat: 52.9608, 
            lng: 36.0583, 
            title: "Сквер танкистов",
            description: "Исторический мемориал"
          },
          { 
            lat: 52.9742, 
            lng: 36.0867, 
            title: "Парк культуры и отдыха",
            description: "Главный парк города"
          },
          { 
            lat: 52.9556, 
            lng: 36.0422, 
            title: "Микрорайон Сталепрокатный",
            description: "Жилой район"
          },
          { 
            lat: 52.9819, 
            lng: 36.0514, 
            title: "Северный район",
            description: "Новый жилой массив"
          }
        ]
  
        points.forEach(point => {
          L.marker([point.lat, point.lng])
            .addTo(map)
            .bindPopup(`
              <div style="min-width: 200px;">
                <h3 style="margin: 0 0 8px 0; color: #333;">${point.title}</h3>
                <p style="margin: 0 0 5px 0; color: #666;">${point.description}</p>
                <small style="color: #999;">Координаты: ${point.lat.toFixed(4)}, ${point.lng.toFixed(4)}</small>
              </div>
            `)
        })
  
        

        // Добавляем границы города (примерные)
        const cityBounds = [
          [52.985, 36.02],
          [52.985, 36.11],
          [52.94, 36.11],
          [52.94, 36.02],
          [52.985, 36.02]
        ]
  
        L.polygon(cityBounds, {
          color: 'green',
          weight: 2,
          opacity: 0.3,
          fillOpacity: 0.1
        }).addTo(map).bindPopup('Город Орёл')
      }
    }
  }
  </script>