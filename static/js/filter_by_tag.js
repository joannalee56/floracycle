// 'use strict'

// let checkedElements = document.querySelectorAll('#tag:checked');
// let allCheckboxes = document.querySelectorAll('#tag');

// let allIsChecked = checkedElements.length === allCheckboxes.length;

// console.log("allIsChecked", allIsChecked);

// if (filter === '*') {
//   animals.forEach(animal => animal.classList.remove('hidden'));
// }

// // full JS code:
// function filterAnimals(e) {
//   const animals = document.querySelectorAll(".list div");
//   let filter = e.target.dataset.filter;
//   if (filter === '*') {
//     animals.forEach(animal => animal.classList.remove('hidden'));
//   }  else {
//     animals.forEach(animal => {
//       animal.classList.contains(filter) ? 
//       animal.classList.remove('hidden') : 
//       animal.classList.add('hidden');
//     });
//   };
// };


// filterClassifieds('.card', '#filter');

// function filterClassifieds(classified, form){


//   const x, i;
//   x = document.getElementsByClassName("card");
//   if (c =="all") c = "";
//   for (i = 0; i < x.length; i++){
//     removeClass(x[i], "show")
//     if (x[i].className.indexOf(c) > -1) addClass(x[i], "show");
//   }
// }

// function addClass(element, name){
//   const i, arr1, arr2;
//   arr1 = element.className.split(" ");
//   arr2 = name.split(" ");
//   for (i=0; i<arr2.length; i++){
//     if(arr1.indexOf(arr2[i]) == -1){
//       element.className += " " + arr2[i];
//     }
//   }
// }

// function removeClass(element, name){
//   const i, arr1, arr2;
//   arr1 = element.className.split(" ");
//   arr2 = name.split(" ");
//   for (i=0; i<arr2.length; i++){
//     while(arr1.indexOf(arr2[i]) > -1){
//       arr1.splice(arr1.indexOf(arr2[i]), 1);
//     }
//   }
//   element.className = arr1.join(" ")
// }


