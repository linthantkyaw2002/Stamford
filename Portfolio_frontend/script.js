// Typed.js Animation
const typed = new Typed(".multipleText", {
    strings: ["Software Engineer", "Web Developer", "IoT Maker"],
    typeSpeed: 100,
    backSpeed: 100,
    backDelay: 1000,
    loop: true,
});

// Fade-in on Scroll
const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
        entry.target.classList.toggle("show-section", entry.isIntersecting);
    });
}, { threshold: 0.2 });

document.querySelectorAll("section").forEach(sec => observer.observe(sec));