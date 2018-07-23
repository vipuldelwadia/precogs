'use strict';

function loadConfig() {
    return firebase.database().ref('/config/').once('value').then(function(snapshot) {
      var question = (snapshot.val() && snapshot.val().question);
        questionTextElement.innerHTML = question;
    });
}

function loadImagesToLabel() {
    var callback = function(snap) {
        var data = snap.val();
        addImageToLabel(snap.key, data.url, data.label);
    };

    firebase.database().ref('/images/').on('child_changed', callback);
    firebase.database().ref('/images/').orderByChild('label').equalTo('').on('child_added', callback);
}
  
function addImageToLabel(name, url, label) {
    if (label == "") {
        var imageToLabel = new Object();
        imageToLabel.name = name;
        imageToLabel.url = url;
        imageToLabel.label = label;
        
        imagesToLabel.push(imageToLabel);
        
        // if we havent set a image to label yet lets use this one.
        if (currentImage == null && imagesToLabel.length >= 10) {
            updateCurrentImage();
        }
    } 
    else {
        var entry;
        for (entry in imagesToLabel) {
            var image = imagesToLabel[entry];
            if (image.name == name) {
                // remove this image from the todo list as someone else bet us to it.
                imagesToLabel.splice(entry, 1);
            }
        }
    }
    updateRemainingWorkCount();
}

function updateCurrentImage() {
    currentImage = randomPop(imagesToLabel); //imagesToLabel.pop();
    if (currentImage) {
        imageElement.src = currentImage.url;
    }
    updateRemainingWorkCount();
}

function updateRemainingWorkCount() {
    remainingWorkCountElement.innerHTML = "" + imagesToLabel.length;
}

function randomPop(array) {
    var randomNumber = Math.floor((Math.random() * array.length));
    var randomObject = array[randomNumber];
    array.splice(randomNumber, 1);
    return randomObject;
}

function checkKey(e) {
    e = e || window.event;
    if (e.keyCode == '37') { // Left cursor pressed.
       noClicked();
    }
    else if (e.keyCode == '39') { // Right cursor pressed.
       yesClicked();
    }
    else if (e.keyCode == '83') { // 'S' pressed
       badClicked();
    }
}

function yesClicked() {
    currentImage.label = "yes";
    updateImageLabel(currentImage);
}

function noClicked() {
    currentImage.label = "no";
    updateImageLabel(currentImage);
}

function badClicked() {
    currentImage.label = "skip";
    updateImageLabel(currentImage);
}

function updateImageLabel(image) {
    firebase.database().ref('/images/' + image.name).child('label')
    .set(image.label);
    
    // Now we have to load the next image to label.
    updateCurrentImage();
}

function imageFailed(event) {
    currentImage.label = "missing";
    updateImageLabel(currentImage);
    updateCurrentImage();
}

// Shortcuts to DOM Elements.
var questionTextElement = document.getElementById('question_header_text');
var imageElement = document.getElementById('image');
var yesButtonElement = document.getElementById('yes_button');
var noButtonElement = document.getElementById('no_button');
var badButtonElement = document.getElementById('bad_button');
var remainingWorkCountElement = document.getElementById('remaining_work_count');

yesButtonElement.addEventListener('click', yesClicked);
noButtonElement.addEventListener('click', noClicked);
badButtonElement.addEventListener('click', badClicked);
imageElement.addEventListener('error', imageFailed);
document.onkeydown = checkKey;

var currentImage;
var imagesToLabel = [];

loadConfig();
loadImagesToLabel();