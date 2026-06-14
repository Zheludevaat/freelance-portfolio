// Form submission handling
const contactForm = document.getElementById('contactForm');

if (contactForm) {
  contactForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Get form values
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;
    
    // Simple validation
    if (name && email && message) {
      // In a real implementation, you would send this data to a server
      alert(`Thank you for your message, ${name}! We'll get back to you soon.`);
      contactForm.reset();
    } else {
      alert('Please fill in all fields.');
    }
  });
}

// Simple test to verify script loading
console.log('Neighbourhood Café site script loaded successfully');