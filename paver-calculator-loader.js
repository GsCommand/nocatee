(function () {
  var originalScript = document.createElement('script');
  originalScript.src = 'https://cdn.jsdelivr.net/gh/GsCommand/nocatee@629be5e76618f4a94ccc3e92f4a82bceb7b2ca90/paver-calculator.js';
  originalScript.onload = function () {
    if (window.location.pathname !== '/' && window.location.pathname !== '/index.html') return;

    var introHeading = Array.prototype.find.call(document.querySelectorAll('main > .section .section-heading h2'), function (heading) {
      return heading.textContent.trim() === 'Paver cleaning and sealing built for Nocatee conditions';
    });
    if (!introHeading) return;

    var resealingParagraph = Array.prototype.find.call(introHeading.closest('.section').querySelectorAll('.home-intro-copy p'), function (paragraph) {
      return paragraph.textContent.indexOf('Paver resealing in Nocatee') !== -1;
    });
    if (!resealingParagraph || resealingParagraph.dataset.seoExpanded === 'true') return;

    resealingParagraph.appendChild(document.createTextNode(' Homeowners searching for professional paver resealing in Nocatee, Ponte Vedra and St. Johns County can rely on HydroSeal for driveway paver resealing, patio paver sealing and pool deck resealing tailored to Florida weather and local surface conditions. A properly prepared paver resealing service can improve curb appeal, reduce joint-sand loss and help extend the usable life of concrete pavers, brick pavers, travertine and natural stone.'));
    resealingParagraph.dataset.seoExpanded = 'true';
  };
  document.head.appendChild(originalScript);
})();
