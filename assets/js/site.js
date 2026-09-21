(function () {
'use strict';
var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
var saveData = navigator.connection && navigator.connection.saveData;
var reveals = document.querySelectorAll('.reveal');
if (reduced || !('IntersectionObserver' in window)) {
Array.prototype.forEach.call(reveals, function (el) { el.classList.add('is-in'); });
} else {
var io = new IntersectionObserver(function (entries) {
entries.forEach(function (e) {
if (!e.isIntersecting) return;
e.target.classList.add('is-in');
io.unobserve(e.target);
});
}, { rootMargin: '0px 0px -12% 0px', threshold: 0.08 });
Array.prototype.forEach.call(reveals, function (el) { io.observe(el); });
}
var spies = document.querySelectorAll('[data-spy]');
var sections = [];
Array.prototype.forEach.call(spies, function (a) {
var s = document.getElementById(a.getAttribute('data-spy'));
if (s) sections.push({ link: a, el: s });
});
function spy() {
var y = window.scrollY + window.innerHeight * 0.35;
var current = null;
sections.forEach(function (s) { if (y >= s.el.offsetTop) current = s; });
sections.forEach(function (s) { s.link.classList.toggle('is-active', s === current); });
}
if (sections.length) {
spy();
window.addEventListener('scroll', function () { window.requestAnimationFrame(spy); }, { passive: true });
}
var galleries = document.querySelectorAll('[data-gallery]');
function embedSrc(id, sound) {
return 'https://www.youtube-nocookie.com/embed/' + id + '?' + [
'autoplay=1', 'mute=' + (sound ? '0' : '1'), 'loop=1', 'playlist=' + id,
'controls=' + (sound ? '1' : '0'), 'modestbranding=1', 'playsinline=1',
'rel=0', 'disablekb=1', 'iv_load_policy=3'
].join('&');
}
function mount(fig, sound) {
if (!fig || !fig.getAttribute('data-yt')) return;
var existing = fig.querySelector('iframe');
if (existing && (fig.dataset.sound === '1') === !!sound) return;
if (existing) existing.remove();
var frame = document.createElement('iframe');
frame.className = 'media__frame';
frame.src = embedSrc(fig.getAttribute('data-yt'), sound);
frame.title = (fig.getAttribute('data-title') || 'Trailer') + ' — trailer';
frame.loading = 'lazy';
frame.allow = 'autoplay; encrypted-media; picture-in-picture';
frame.setAttribute('allowfullscreen', '');
fig.appendChild(frame);
fig.dataset.sound = sound ? '1' : '0';
fig.classList.add('is-playing');
if (sound) fig.classList.add('has-sound');
}
function unmount(fig) {
if (!fig) return;
var frame = fig.querySelector('iframe');
if (frame) frame.remove();
fig.classList.remove('is-playing', 'has-sound');
delete fig.dataset.sound;
}
Array.prototype.forEach.call(galleries, function (gal) {
var slides = gal.querySelectorAll('.media');
var dots = gal.querySelectorAll('.dot');
var label = gal.querySelector('[data-gallery-label]');
var inView = false;
function active() { return gal.querySelector('.media.is-active'); }
function select(i) {
var prev = active();
if (prev === slides[i]) return;
unmount(prev);
Array.prototype.forEach.call(slides, function (s, n) { s.classList.toggle('is-active', n === i); });
Array.prototype.forEach.call(dots, function (d, n) { d.setAttribute('aria-selected', n === i ? 'true' : 'false'); });
if (label) {
label.innerHTML = (i + 1) + ' / ' + slides.length + ' &nbsp; ' +
(slides[i].getAttribute('data-title') || '').toUpperCase();
}
if (inView && !reduced && !saveData) mount(slides[i], false);
}
Array.prototype.forEach.call(dots, function (d, i) {
d.addEventListener('click', function () { select(i); });
});
function step(dir) {
var cur = Array.prototype.indexOf.call(slides, active());
select((cur + dir + slides.length) % slides.length);
}
var prev = gal.querySelector('[data-prev]');
var next = gal.querySelector('[data-next]');
if (prev) prev.addEventListener('click', function () { step(-1); });
if (next) next.addEventListener('click', function () { step(1); });
if (slides.length > 1) {
var sx = 0, sy = 0, tracking = false;
gal.addEventListener('touchstart', function (e) {
if (e.touches.length !== 1) return;
sx = e.touches[0].clientX;
sy = e.touches[0].clientY;
tracking = true;
}, { passive: true });
gal.addEventListener('touchend', function (e) {
if (!tracking) return;
tracking = false;
var t = e.changedTouches[0];
var dx = t.clientX - sx, dy = t.clientY - sy;
if (Math.abs(dx) < 40 || Math.abs(dx) < Math.abs(dy)) return;
var cur = Array.prototype.indexOf.call(slides, active());
select(dx < 0 ? (cur + 1) % slides.length : (cur - 1 + slides.length) % slides.length);
}, { passive: true });
}
gal.addEventListener('keydown', function (e) {
if (!dots.length) return;
var cur = Array.prototype.indexOf.call(slides, active());
if (e.key === 'ArrowRight') { select((cur + 1) % slides.length); dots[(cur + 1) % slides.length].focus(); }
if (e.key === 'ArrowLeft') { select((cur - 1 + slides.length) % slides.length); dots[(cur - 1 + slides.length) % slides.length].focus(); }
});
if (!reduced && !saveData && 'IntersectionObserver' in window) {
new IntersectionObserver(function (entries) {
entries.forEach(function (e) {
inView = e.isIntersecting;
if (inView) mount(active(), false);
else unmount(active());
});
}, { rootMargin: '150px 0px 150px 0px', threshold: 0.35 }).observe(gal);
}
});
document.addEventListener('click', function (ev) {
var btn = ev.target.closest ? ev.target.closest('.media__sound') : null;
if (!btn) return;
mount(btn.closest('.media'), true);
});
document.addEventListener('click', function (ev) {
var btn = ev.target.closest ? ev.target.closest('.wf-gif') : null;
if (!btn || btn.classList.contains('is-playing')) return;
var src = btn.getAttribute('data-gif');
var img = btn.querySelector('img');
if (!src || !img) return;
btn.classList.add('is-loading');
var full = new Image();
full.onload = function () {
img.src = src;
btn.classList.remove('is-loading');
btn.classList.add('is-playing');
};
full.src = src;
});
var clips = document.querySelectorAll('video[data-autoplay]');
if (clips.length && 'IntersectionObserver' in window) {
var cio = new IntersectionObserver(function (entries) {
entries.forEach(function (e) {
var v = e.target;
if (e.isIntersecting) {
if (v.preload !== 'auto') { v.preload = 'auto'; v.load(); }
var p = v.play();
if (p && p.catch) p.catch(function () {});
} else if (!v.paused) {
v.pause();
}
});
}, { rootMargin: '200px 0px', threshold: 0.25 });
Array.prototype.forEach.call(clips, function (v) { cio.observe(v); });
}
document.addEventListener('click', function (ev) {
var b = ev.target.closest ? ev.target.closest('[data-mail]') : null;
if (!b) return;
var addr = b.getAttribute('data-u') + String.fromCharCode(64) + b.getAttribute('data-d');
var subject = b.getAttribute('data-s');
window.location.href = 'mailto:' + addr + (subject ? '?subject=' + encodeURIComponent(subject) : '');
});
Array.prototype.forEach.call(document.querySelectorAll('[data-mail]'), function (b) {
var show = function () {
b.title = b.getAttribute('data-u') + String.fromCharCode(64) + b.getAttribute('data-d');
};
b.addEventListener('mouseenter', show);
b.addEventListener('focus', show);
});
var coarse = window.matchMedia('(pointer: coarse)').matches;
if (reduced || coarse) return;
var STEP = 26;        // px of travel between bones
var LIFE = 900;       // ms from spawn to gone
var MAX = 34;         // hard ceiling on live bones
var IDLE = 900;       // ms of stillness before the loop parks itself
var COLORS = ['#f8f8f2', '#bd93f9', '#ff79c6', '#8be9fd'];
var SVG = '<svg viewBox="0 0 40 17" width="W" height="H" fill="C" aria-hidden="true">' +
'<rect x="4" y="5.5" width="32" height="6" rx="3"></rect>' +
'<circle cx="4.5" cy="4.5" r="4.5"></circle><circle cx="4.5" cy="12.5" r="4.5"></circle>' +
'<circle cx="35.5" cy="4.5" r="4.5"></circle><circle cx="35.5" cy="12.5" r="4.5"></circle></svg>';
var pointer = null;   // live pointer position
var emit = null;      // last position a bone was dropped at
var live = [];
var colorIndex = 0;
var lastMove = 0;
var running = false;
function rand(min, max) { return min + Math.random() * (max - min); }
window.addEventListener('pointermove', function (e) {
if (e.pointerType === 'touch') return;
pointer = { x: e.clientX, y: e.clientY };
if (!emit) emit = { x: pointer.x, y: pointer.y };
lastMove = performance.now();
if (!running) { running = true; requestAnimationFrame(frame); }
}, { passive: true });
document.addEventListener('pointerleave', function () { pointer = null; emit = null; });
window.addEventListener('blur', function () { pointer = null; emit = null; });
function frame(now) {
if (!pointer || !emit) { running = false; return; }
var dx = pointer.x - emit.x;
var dy = pointer.y - emit.y;
var dist = Math.sqrt(dx * dx + dy * dy);
while (dist >= STEP) {
var t = STEP / dist;
emit.x += dx * t;
emit.y += dy * t;
spawn(emit.x, emit.y);
dx = pointer.x - emit.x;
dy = pointer.y - emit.y;
dist = Math.sqrt(dx * dx + dy * dy);
}
if (now - lastMove > IDLE) { running = false; return; }
requestAnimationFrame(frame);
}
function spawn(x, y) {
while (live.length >= MAX) {
var old = live.shift();
if (old && old.parentNode) old.parentNode.removeChild(old);
}
var w = rand(11, 24);   // small, and no two the same
var h = w * 0.42;
var rot = rand(0, 360);                 // every bone lies at its own angle
var tumble = rot + rand(-90, 90);       // and keeps turning while it fades
var driftX = rand(-12, 12);
var driftY = rand(6, 24);
var color = COLORS[colorIndex++ % COLORS.length];
var b = document.createElement('div');
b.className = 'bone';
b.innerHTML = SVG.replace('W', w.toFixed(1)).replace('H', h.toFixed(1)).replace('C', color);
var px = x - w / 2, py = y - h / 2;
b.style.transform = 'translate(' + px.toFixed(1) + 'px,' + py.toFixed(1) + 'px) rotate(' + rot.toFixed(1) + 'deg)';
b.style.opacity = '0.95';
document.body.appendChild(b);
live.push(b);
requestAnimationFrame(function () {
b.style.transition = 'opacity ' + LIFE + 'ms linear, transform ' + LIFE + 'ms cubic-bezier(.22,.7,.3,1)';
b.style.opacity = '0';
b.style.transform = 'translate(' + (px + driftX).toFixed(1) + 'px,' + (py + driftY).toFixed(1) + 'px) ' +
'rotate(' + tumble.toFixed(1) + 'deg) scale(.7)';
});
setTimeout(function () {
var i = live.indexOf(b);
if (i > -1) live.splice(i, 1);
if (b.parentNode) b.parentNode.removeChild(b);
}, LIFE + 60);
}
})();