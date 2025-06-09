(function() {
  const container = document.querySelector('.animated-bg');
  if (!container) return;
  const count = 30;
  for (let i = 0; i < count; i++) {
    const particle = document.createElement('span');
    particle.className = 'particle';
    particle.style.left = Math.random() * 100 + '%';
    particle.style.animationDelay = Math.random() * 5 + 's';
    particle.style.fontSize = 12 + Math.random() * 20 + 'px';
    particle.textContent = ['λ','Σ','∑','π','β','∂'][Math.floor(Math.random()*6)];
    container.appendChild(particle);
  }
})();
