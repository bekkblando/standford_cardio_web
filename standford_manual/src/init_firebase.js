import Firebase from 'firebase';

// Initialize Firebase
var config = {
  apiKey: "AIzaSyCVj9ZWunoXIGOT08Qw8XF9qiS_TTnsP8A",
  authDomain: "stanford-heart-surgery.firebaseapp.com",
  databaseURL: "https://stanford-heart-surgery.firebaseio.com",
  projectId: "stanford-heart-surgery",
  storageBucket: "stanford-heart-surgery.appspot.com",
  messagingSenderId: "856277829656"
};

var firebase = Firebase.initializeApp(config);


export default firebase;
