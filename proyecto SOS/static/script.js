document.addEventListener('DOMContentLoaded', () => {
    // Navigation Logic
    const navBtns = document.querySelectorAll('.nav-btn');
    const sections = document.querySelectorAll('main section');

    function switchSection(targetId) {
        navBtns.forEach(b => {
            if (b.getAttribute('data-target') === targetId) {
                b.classList.add('active');
            } else {
                b.classList.remove('active');
            }
        });
        sections.forEach(s => s.classList.remove('active-section'));
        document.getElementById(targetId).classList.add('active-section');
    }

    navBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Note: btn can target a section that isn't mapped to a tab exactly
            const targetId = btn.getAttribute('data-target');
            switchSection(targetId);
        });
    });

    // Toast Logic
    const toast = document.getElementById('toast-message');
    function showToast(message, duration = 5000) {
        toast.textContent = message;
        toast.classList.remove('hidden');
        setTimeout(() => {
            toast.classList.add('hidden');
        }, duration);
    }

    // Geolocation Logic
    let currentLat = null;
    let currentLng = null;
    function getLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    currentLat = position.coords.latitude;
                    currentLng = position.coords.longitude;
                },
                (error) => {
                    console.log("Error al obtener ubicación.");
                }
            );
        }
    }
    getLocation();

    // SOS Button Logic
    const sosBtn = document.getElementById('sos-btn');
    const modal = document.getElementById('emergency-modal');
    sosBtn.addEventListener('click', () => {
        if (!currentLat) getLocation();
        modal.classList.remove('hidden');
    });

    // Form Submission
    const emergencyForm = document.getElementById('emergency-form');
    const submitBtn = emergencyForm.querySelector('.submit-btn');
    const iaText = document.getElementById('ia-recommendation-text');
    const backToSosBtn = document.getElementById('back-to-sos-btn');

    emergencyForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const payload = {
            nombre: document.getElementById('f-nombre').value,
            apellido: document.getElementById('f-apellido').value,
            edad: document.getElementById('f-edad').value,
            telefono: document.getElementById('f-telefono').value,
            tipo_usuario: document.getElementById('f-tipo').value,
            resumen: document.getElementById('f-resumen').value,
            lat: currentLat,
            lng: currentLng
        };

        // UI Feedback during request
        submitBtn.textContent = "Procesando...";
        submitBtn.disabled = true;

        try {
            const response = await fetch('/api/sos', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await response.json();
            
            if(data.status === 'success') {
                modal.classList.add('hidden');
                
                // Show 5 seconds toast
                showToast("¡ALERTA ENVIADA A LAS AUTORIDADES!");
                
                // Redirect to IA Recommendation Section
                iaText.textContent = data.recomendacion;
                switchSection('ia-section');
                
                // Clean form
                emergencyForm.reset();
            }
        } catch (err) {
            showToast("Error de red. Asegúrese de tener conexión.", 3000);
            toast.style.background = "#ef4444";
        } finally {
            submitBtn.textContent = "Enviar Alerta Inmediata";
            submitBtn.disabled = false;
        }
    });

    // Back to SOS
    backToSosBtn.addEventListener('click', () => {
        switchSection('sos-section');
    });
});
