// // On mobile devices, change the y-translate of the img.project-tile-image when the user scrolls so that the image appears to move slower than the rest of the page
// // Use plain JavaScript

// var projectTileImages = document.querySelectorAll('img.project-tile-image');
// var projectTileImagesArray = Array.from(projectTileImages);

// // The scroll factor determines how much the image will move relative to the rest of the page.
// const scrollFactor = 0.1;

// // Determine if the image scrolling direction is reversed
// var scrollDirectionReversed = false;

// // Compute the image zoom factor and the maximum translation of the image from the scroll factor
// // If the scroll factor is 0, the image will be zoomed in by a factor of 1 and will not move
// // If the scroll factor is 1/2, the image will be zoomed in by a factor of 2 and will move from +25% to -25% of its original position
// // If the scroll factor is 1/3, the image will be zoomed in by a factor of 1.5 and will move from +15.6% to -15.6% of its original position
// zoomFactor = 1 / (1 - scrollFactor); 
// maxTranslation = 100 / 2 * scrollFactor;

// function getMaxScollPosition() {
//     return document.body.scrollHeight - window.innerHeight;
// }

// function computeTransformPercent(scrollPosition) {
//     if (scrollDirectionReversed) {
//         return ((1 - (scrollPosition / getMaxScollPosition())) * (maxTranslation * 2) - maxTranslation);
//     } else {
//         return ((scrollPosition / getMaxScollPosition()) * (maxTranslation * 2) - maxTranslation);
//     }
// }

// function translateImage() {
//     // Only run the function if the device is a mobile device
//     if (window.innerWidth < 808) {
//         projectTileImagesArray.forEach(function(image) {
//             // Remove the zoom-on-hover class from the image
//             image.classList.remove('zoom-on-hover');

//             // Set the transform of the image
//             image.style.transform = 'scale(' + zoomFactor + ') translate(0,' + computeTransformPercent(window.scrollY) + '%)';
//             console.log(getComputedStyle(image).transform);
//         });
//     } else {
//         projectTileImagesArray.forEach(function(image) {
//             // Add the zoom-on-hover class to the image
//             image.classList.add('zoom-on-hover');

//             // Reset the transform of the image
//             image.style.transform = 'scale(1) translate(0,0)';
//         });
//     }
// }


// // Run the function on page load
// translateImage();

// // Run the function on scroll
// window.addEventListener('scroll', translateImage)

// // Also run the function on resize
// window.addEventListener('resize', translateImage);
