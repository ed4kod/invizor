document.addEventListener('DOMContentLoaded', function() {
  const brand = document.querySelector('.navbar-brand');
  const eyeClosed = document.getElementById('eye-closed');
  const eyeOpen = document.getElementById('eye-open');
  if (brand && eyeClosed && eyeOpen) {
    brand.addEventListener('mouseenter', function() {
      eyeClosed.style.display = 'none';
      eyeOpen.style.display = 'flex';
    });
    brand.addEventListener('mouseleave', function() {
      eyeClosed.style.display = 'flex';
      eyeOpen.style.display = 'none';
    });
  }
}); 