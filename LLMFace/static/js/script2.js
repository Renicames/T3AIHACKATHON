document.addEventListener('DOMContentLoaded', function() {
    // Bütün linkleri yakalayın ve her biri için event listener ekleyin
    const links = document.querySelectorAll('.nav-link');
    
    links.forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault(); // Varsayılan link davranışını durdurur.
            const targetUrl = link.getAttribute('href'); // href değerini al
            window.location.href = targetUrl; // Yönlendirme yapılacak URL.
        });
    });
    
    // "Başla" butonu için ayrıca bir event listener
    const startBtn = document.getElementById('start-btn');
    if (startBtn) {
        startBtn.addEventListener('click', function(event) {
            event.preventDefault();
            window.location.href = "/chat";
        });
    }
});
