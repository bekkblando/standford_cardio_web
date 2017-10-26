import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import registerServiceWorker from './registerServiceWorker';
import Firebase from 'firebase';
import './index.css';

// Initialize Firebase
var config = {
  // Credentials Here
};

var firebase = Firebase.initializeApp(config);

// TODO This is not ideal - Needed for demo
firebase.auth().signInWithEmailAndPassword("fakeemail", "FakePass")

// Get the manual
var manual_ref = firebase.database().ref().child("manual");

ReactDOM.render(<App manual_ref={manual_ref}/>, document.getElementById('root'));
registerServiceWorker();

manual_ref.on("value", function(manual) {
  var output_text = manual.val();

  // Not an ideal way of loading the manual
  document.getElementById("manual").innerHTML = output_text;

}, function (errorObject) {
  // Failed
  console.log("The read failed: " + errorObject.code);
});
